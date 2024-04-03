export type SiteConfig = typeof siteConfig

export const siteConfig = {
    name: "DVerse",
    description:
        "A pair of collaborating bots called DVerse.",
    mainNav: [
        {
            title: "Chat",
            href: "/",
        }, {
            title: "Explore",
            href: "/",
        }, {
            title: "Contact",
            href: "/contact",
        },
    ],
    links: {
        masterdon: "https://dverse.masto.host/home",
        github: "https://github.com/fuas-dverse/DVerse",
        docs: "https://fuas-dverse.github.io/",
    },
}