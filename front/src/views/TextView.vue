<template>
    <v-card id="textView">
        <v-card-title> {{ text.title }} </v-card-title>
        <v-card-subtitle> {{ text._id }} </v-card-subtitle>
        <v-card-text>
            <template v-for="sentenceObj in sentenceObjts">
                <router-link
                    :key="sentenceObj._id"
                    @mouseover.native="hover = true"
                    @mouseleave.native="hover = false"
                    :to="{
                        name: 'SentenceComparison',
                        params: {
                            sentenceID: sentenceObj._id,
                            sentence: sentenceObj.sentence
                        }
                    }"
                    style="text-decoration: none; color: black;"
                >
                    {{ sentenceObj.sentence }}
                </router-link>
            </template>
        </v-card-text>
    </v-card>
</template>

<script>
import { api } from "@/utils/HTTPTransport";

export default {
    name: "TextView",

    data() {
        return {
            text: this.$route.params.text,
            sentenceObjts: []
        };
    },
    async mounted() {
        this.sentenceObjts = await api.getTextSentences(
            this.$route.params.text._id
        );
    }
};
</script>

<style></style>
