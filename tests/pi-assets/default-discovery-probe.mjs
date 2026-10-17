import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const [agentDir, project] = process.argv.slice(2);
const root = process.env.PI_SDK_ROOT;
const { DefaultResourceLoader } = await import(pathToFileURL(join(root, 'dist/core/resource-loader.js')));
const { formatSkillsForPrompt } = await import(pathToFileURL(join(root, 'dist/core/skills.js')));
const { SettingsManager } = await import(pathToFileURL(join(root, 'dist/core/settings-manager.js')));
const settingsManager = SettingsManager.create(project, agentDir, { projectTrusted: false });
const loader = new DefaultResourceLoader({ cwd: project, agentDir, settingsManager, noExtensions: true, noPromptTemplates: true, noThemes: true });
async function snapshot() {
  await loader.reload();
  const { skills, diagnostics } = loader.getSkills();
  const { agentsFiles } = loader.getAgentsFiles();
  return {
    names: skills.map(skill => skill.name).sort(),
    diagnostics,
    prompt: formatSkillsForPrompt(skills),
    explicitOnly: skills.filter(skill => skill.disableModelInvocation).map(skill => skill.name).sort(),
    globalContext: agentsFiles.some(file => file.path === join(agentDir, 'AGENTS.md')),
    projectContext: agentsFiles.some(file => file.path === join(project, 'AGENTS.md')),
  };
}
const untrusted = await snapshot();
settingsManager.setProjectTrusted(true);
const trusted = await snapshot();
const { createAgentSession } = await import(pathToFileURL(join(root, 'dist/core/sdk.js')));
const { SessionManager } = await import(pathToFileURL(join(root, 'dist/core/session-manager.js')));
const { ModelRuntime } = await import(pathToFileURL(join(root, 'dist/core/model-runtime.js')));
const { AuthStorage } = await import(pathToFileURL(join(root, 'dist/core/auth-storage.js')));
const modelRuntime = await ModelRuntime.create({ credentials: AuthStorage.inMemory(), modelsPath: null, refreshOnCreate: false, allowModelNetwork: false });
const model = modelRuntime.getModel('openai', 'gpt-5');
if (!model) throw new Error('Static native test model is unavailable');
const { session } = await createAgentSession({ cwd: project, agentDir, modelRuntime, model, resourceLoader: loader, settingsManager, sessionManager: SessionManager.inMemory(project), tools: [] });
try {
  // Public queue expansion does not start a turn or request provider credentials.
  await session.steer('/skill:text-prune Tighten the supplied synthetic paragraph.');
  const [textPruneExpansion] = session.getSteeringMessages();
  console.log(JSON.stringify({ untrusted, trusted, textPruneExpansion }));
} finally {
  session.dispose();
}
