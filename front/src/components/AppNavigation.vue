<template>
    <div id="nav">
        <v-navigation-drawer
            app
            v-model="drawer"
            color="#414A4F"
            dark
            disable-resize-watcher
        >
            <v-list nav>
                <template v-for="(item, index) in NavButtons">
                    <v-list-item
                        :key="`nav-draw-item-${index}`"
                        link
                        :to="item.route"
                        @click="item.action"
                    >
                        <v-list-item-icon>
                            <v-icon> {{ item.icon }} </v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            {{ item.title }}
                        </v-list-item-content>
                    </v-list-item>
                    <v-divider :key="`divider-${index}`"></v-divider>
                </template>
            </v-list>
        </v-navigation-drawer>
        <v-app-bar app color="#32637A" dark>
            <v-app-bar-nav-icon @click="drawer = !drawer"> </v-app-bar-nav-icon>
            <v-spacer></v-spacer>
            <v-toolbar-title>{{ appTitle }}</v-toolbar-title>
            <v-spacer></v-spacer>
            <connection-indicator />
        </v-app-bar>
        <add-text-form></add-text-form>
    </div>
</template>

<script>
import AddTextForm from "@/components/AddTextForm";
import ConnectionIndicator from "@/components/ConnectionIndicator";

export default {
    name: "AppNavigation",
    data() {
        return {
            appTitle: "Text Matcher",
            drawer: false,
            logs: [],
            NavButtons: [
                {
                    title: "Home",
                    action: () => void 0,
                    route: { name: "Home" },
                    icon: "mdi-view-dashboard"
                },
                {
                    title: "Add new text",
                    action: this.addNewTextAction,
                    route: "",
                    icon: "mdi-plus"
                },
                {
                    title: "About",
                    action: this.aboutAction,
                    route: "",
                    icon: "mdi-information"
                }
            ]
        };
    },
    components: {
        AddTextForm,
        ConnectionIndicator
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
#nav .v-list-item--link {
    font-weight: bold;
    color: #fba85c;
    padding: 0 10px;
    text-decoration: none;
}
#nav .v-list-item--active {
    font-weight: bold;
    color: #fe6625;
    padding: 0 10px;
}
</style>
