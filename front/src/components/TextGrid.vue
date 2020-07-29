<template>
    <div>
        <v-container fluid>
            <v-row>
                <template v-for="text in texts">
                    <v-col cols="4" :key="text._id">
                        <text-card :text="text"></text-card>
                    </v-col>
                </template>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import TextCard from "@/components/TextCard";
import { api } from "@/utils/HTTPTransport";

export default {
    name: "TextGrid",
    computed: {
        textToSend() {
            return this.$store.textToSend;
        },
        texts() {
            return this.$store.getters.texts;
        }
    },
    components: {
        TextCard
    },
    created() {
        // initial data fetching
        api.getTexts()
            .then(response => {
                response.forEach(textElem => {
                    this.$store.commit("pushText", textElem);
                });
            })
            .catch(error => {
                console.log(`Error: ${error}`);
            });
    }
};
</script>

<style></style>
