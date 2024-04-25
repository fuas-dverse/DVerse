# Frontend DVerse - Prototype 3

This part of the repository contains the code for the frontend of the DVerse project. This is a NextJS project using
TypeScript. We chose NextJS as the framework because of its ease of setup and our team's familiarity with it. This
project uses the [Shadcn](https://ui.shadcn.com/) component library for easily creating the UI.

## Requirements

To run this project locally, you will need the following:

- Node.js (version 14 or later)
- npm (version 6 or later) or yarn (version 1.22 or later)
- A modern web browser

Ensure Node.js and npm/yarn are installed by running `node -v` and `npm -v` or `yarn -v` in your terminal. If these
commands fail, you need to install Node.js and npm/yarn.

## Development

Before you can run the project, you need to install its dependencies. Navigate to the project directory in your terminal
and run:

```bash
npm install
```

or if you prefer yarn:

```shell
yarn install
```

## Setup Keycloak
This project contains keycloak for authentication. In order to start developing you need to setup Keycloak using this tutorial:
https://github.com/fuas-dverse/DVerse-UI/wiki/Setup-Keycloak

## Environment Variables

This project may require certain environment variables to be set up for API calls or other features. Rename the
.env.example file to .env.local and fill in the necessary values.

## Running the Project Locally

To start the development server, run:

````shell
npm run dev
````

or if you are using yarn:

````shell
yarn dev
````

This will start the NextJS development server on http://localhost:3000. Open your browser and navigate to this URL to
see the application running.

# Contributing

We welcome contributions to the DVerse frontend! Please read the following instructions before making pull requestst.

- We make use of [Shadcn](https://ui.shadcn.com/), this means that all components are already there. When you want to
  create a new page or component, you must use the
  predefined [components](https://ui.shadcn.com/docs/components/accordion) from Shadcn. This way we keep the styling
  structured and the same all over the project.
- Please read the NextJS documentation first before developing the code yourself. NextJS has some internal features that
  can be helpful in developing clean code such
  as: [Data fetching](https://nextjs.org/docs/app/building-your-application/data-fetching), [Rendering](https://nextjs.org/docs/app/building-your-application/rendering)
  on the server or client, [Testing](https://nextjs.org/docs/app/building-your-application/testing) and more...
- You can't push to main instantly, so you have to checkout to another branch that has a good understanding what you are
  making. Form here you can create a pull request and it needs to be reviewed by at least one member.

## Authors
- [Marc van Grootel](https://github.com/xokomola)
- [Brett Mulder](https://github.com/Brett-Mulder)
- [Reno Muijsenberg](https://github.com/renomuijsenberg)
- [Bas Onrust](https://github.com/Saprone)
- [Arenco Meevissen](https://github.com/AmFontys)
- [Iulia Toderaşcu](https://github.com/iuliaToderascu)