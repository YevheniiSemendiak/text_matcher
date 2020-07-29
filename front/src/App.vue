<template>
    <v-app>
        <app-navigation></app-navigation>
        <v-main>
            <router-view />
            <alert-notifier />
        </v-main>
        <v-footer></v-footer>
    </v-app>
</template>

<script>
import AppNavigation from "@/components/AppNavigation";
import AlertNotifier from "@/components/AlertNotifier";

export default {
    name: "App",
    components: {
        AppNavigation,
        AlertNotifier
    },
    watch: {
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        $route(to, from) {
            document.title = "TextMacher | " + to.meta.title;
        }
    },
    created() {
        this.$store.getters.wStomp.connect(
            "guest", // user
            "guest", // pass
            () => void 0,
            frame => void 0,
            "/"
        );
    },
    destroyed() {
        this.$store.getters.wStomp.disconnect(this.logEvent);
    }
};
</script>
<style></style>
