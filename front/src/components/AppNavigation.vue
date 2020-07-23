<template>
    <div id="nav">
        <v-navigation-drawer
            app
            v-model="drawer"
            class="#414A4F"
            dark
            disable-resize-watcher
        >
            <v-list rounded>
                <template v-for="(item, index) in NavButtons">
                    <v-list-item-title :key="index">
                        <v-list-item-content @click="item.action">
                            <router-link
                                class="d-flex justify-center"
                                :to="item.route"
                            >
                                {{ item.title }}
                            </router-link>
                        </v-list-item-content>
                    </v-list-item-title>
                    <v-divider :key="`divider-${index}`"></v-divider>
                </template>
            </v-list>
        </v-navigation-drawer>
        <v-app-bar app color="#32637A" dark>
            <v-app-bar-nav-icon @click="drawer = !drawer"> </v-app-bar-nav-icon>
            <v-spacer></v-spacer>
            <v-toolbar-title>{{ appTitle }}</v-toolbar-title>
            <v-spacer></v-spacer>
        </v-app-bar>
        <add-text-form></add-text-form>
    </div>
</template>

<script>
import AddTextForm from "@/components/AddTextForm";

export default {
    name: "AppNavigation",
    data() {
        return {
            appTitle: "Text Matcher",
            drawer: false,
            logs: [],
            NavButtons: [
                { title: "Home", action: () => void 0, route: "/" },
                {
                    title: "Add new text",
                    action: this.addNewTextAction,
                    route: ""
                },
                { title: "About", action: this.aboutAction, route: "" }
            ]
        };
    },
    components: {
        AddTextForm
    },
    methods: {
        addNewTextAction() {
            this.$store.commit("flipAddTextFormShown");
        },
        aboutAction() {
            window.open(
                "https://github.com/YevheniiSemendiak/text_matcher#usage"
            );
        }
    }
};
</script>
<style scoped>
#nav a {
    font-weight: bold;
    color: #2c3e50;
    padding: 0 10px;
}
#nav a.router-link-active {
    font-weight: bold;
    color: #fba85c;
    padding: 0 10px;
    text-decoration: none;
}

#nav a.router-link-exact-active {
    font-weight: bold;
    color: #fe6625;
    padding: 0 10px;
}
</style>
