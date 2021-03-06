import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
    {
        path: "/",
        name: "Home",
        component: () =>
            import(/* webpackChunkName: "Home" */ "@/views/Home.vue"),
        meta: {
            title: "Home"
        }
    },
    {
        path: "/text-view",
        name: "TextView",
        component: () =>
            import(/* webpackChunkName: "TextView" */ "@/views/TextView.vue"),
        meta: {
            title: "Text View"
        }
    },
    {
        path: "/sentence-comparison",
        name: "SentenceComparison",
        component: () =>
            import(
                /* webpackChunkName: "SentenceComparison" */ "@/views/SentenceComparison.vue"
            ),
        meta: {
            title: "Sentence Comparison"
        }
    }
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes
});

export default router;
