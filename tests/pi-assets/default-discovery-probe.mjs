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
console.log(JSON.stringify({ untrusted, trusted }));
