
# Dev progress (Nuxt + PrimeVue)

## Install

```bash
$ npx nuxi init {project-name}

$ cd {project-name}

$ npm install primevue

$ npm install primeicons

$ npm install primeflex --save
```

## Config

### nuxt.config.ts

```ts
export default defineNuxtConfig({
    css: [
        "primevue/resources/themes/tailwind-light/theme.css",
        "primevue/resources/primevue.css",
        "primeicons/primeicons.css",//add this to css list , if you want to use primeicons
        "primeflex/primeflex.css"
    ],
	build: {
		transpile: ["primevue"],
	}
})
```

## Plugins

If you want to use some components globally, you can use plugins.
And more details, you can see [here](https://primevue.org/megamenu/).

## Run

```bash
$ npm run dev -o
```