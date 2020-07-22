<template>
    <div>
        <v-navigation-drawer
            app
            v-model="drawer"
            class="teal darken-1"
            dark
            disable-resize-watcher
        >
            <v-list rounded>
                <template v-for="(item, index) in items">
                    <v-list-item-title :key="index">
                        <v-list-item-content
                            @click="item.action"
                            class="d-flex justify-center"
                        >
                            {{ item.title }}
                        </v-list-item-content>
                    </v-list-item-title>
                    <v-divider :key="`divider-${index}`"></v-divider>
                </template>
            </v-list>
        </v-navigation-drawer>
        <v-app-bar app color="teal" dark>
            <v-app-bar-nav-icon
                class="hidden-md-and-up"
                @click="drawer = !drawer"
            >
            </v-app-bar-nav-icon>
            <v-spacer class="hidden-md-and-up"></v-spacer>
            <v-btn
                color="teal lighten-1"
                class="hidden-sm-and-down"
                @click="addNewTextAction"
            >
                Add new text</v-btn
            >
            <v-spacer class="hidden-sm-and-down"></v-spacer>
            <v-toolbar-title>{{ appTitle }}</v-toolbar-title>
            <v-spacer class="hidden-sm-and-down"></v-spacer>
            <v-btn
                color="teal lighten-1"
                class="hidden-sm-and-down"
                @click="aboutAction"
                >About</v-btn
            >
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
            items: [
                { title: "Add new text", action: this.addNewTextAction },
                { title: "About", action: this.aboutAction }
            ],
            showAddTextForm: false
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
<style scoped></style>
