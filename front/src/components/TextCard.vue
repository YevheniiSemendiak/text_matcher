<template>
    <v-hover v-slot:default="{ hover }">
        <router-link
            style="text-decoration: none; color: inherit;"
            :to="{
                name: 'TextView',
                params: { text: text }
            }"
        >
            <v-card :elevation="hover ? 12 : 2">
                <v-card-title> {{ text.title }} </v-card-title>
                <v-card-subtitle>
                    {{
                        new Date(text.dateAdded).toISOString().substring(0, 10)
                    }}
                </v-card-subtitle>
                <v-card-text>
                    <div class="textOverflowing">
                        {{ text.text }}
                    </div></v-card-text
                >
            </v-card>
        </router-link>
    </v-hover>
</template>

<script>
import router from "../router";
export default {
    name: "TextCard",
    props: {
        text: {
            default: "Undefined"
        }
    },
    data() {
        return {
            // cardMaxHeigh: window.innerHeight / 4,
            // cardMaxWidth: window.innerWidth / 3 - window.innerWidth * 0.1
        };
    },
    methods: {
        openTextView() {
            router.openTextView;
        }
    }
};
</script>

<style lang="scss" scoped>
.textOverflowing {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 5; /* number of lines to show */
    -webkit-box-orient: vertical;
}
</style>
