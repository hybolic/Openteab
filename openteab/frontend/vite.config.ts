import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'

const replaceRegex = /@REPLACE\s+'([^']*)'\s+WITH\s+'([^']*)'/g
const replace_devonly_and_replace = /^[ \t]*\*?[ \t]*@(DEV-ONLY|REPLACE).*$/gm

function devOnlyTransform() {
  return {
    name: 'dev-only-transform',

    transform(code: string, id: string) {
      //file not typescript exit early
      if (!id.endsWith('.ts') && !id.endsWith('.tsx')) return
      //file does not contain the dev-only command exit early
      if (!code.includes("@DEV-ONLY")) return

      //get replace with matches
      const replacements = [...code.matchAll(replaceRegex)]
      if (replacements.length > 0)
      {
        //replace built list of replacements
        for (const [, from, to] of replacements)
          code = code.replaceAll(from, to)

        // Remove the build instructions
        code = code.replace(replace_devonly_and_replace, '')

        return { code, map: null }
      }
    },
  }
}
// https://vite.dev/config/
export default defineConfig({
  base: "./",
  plugins: [react(), devOnlyTransform(), viteSingleFile()],
  server: {
    port: 5555,
  },
  //used to help find issues before its minified
  // esbuild: {
  //   pure: ['console.log'],    // example: have esbuild remove any console.log
  //   minifyIdentifiers: false, // but keep variable names
  // },
  // build: {
  //     minify: 'esbuild',
  // }
})
