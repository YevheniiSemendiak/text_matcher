<template>
    <v-hover v-slot:default="{ hover }">
        <v-card :elevation="hover ? 12 : 2">
            <v-card-title> {{ title }} </v-card-title>
            <v-card-subtitle> {{ id }} </v-card-subtitle>
            <v-card-text>
                <div class="textOverflowing">{{ text }}</div></v-card-text
            >
        </v-card>
    </v-hover>
</template>

<script>
export default {
    name: "TextCard",
    props: {
        title: {
            default: "Undefined",
            type: String
        },
        text: {
            default: "Undefined",
            type: String
        },
        id: {
            required: true,
            type: String
        }
    },
    data() {
        return {
            // cardMaxHeigh: window.innerHeight / 4,
            // cardMaxWidth: window.innerWidth / 3 - window.innerWidth * 0.1
        };
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
