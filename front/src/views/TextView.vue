<template>
    <v-card>
        <v-card-title> {{ title }} </v-card-title>
        <v-card-subtitle> {{ id }} </v-card-subtitle>
        <v-card-text> {{ text }}</v-card-text>
    </v-card>
</template>

<script>
export default {
    name: "TextView",
    data() {
        return {
            title: this.$route.params.title,
            id: this.$route.params.id,
            text: this.$route.params.text
        };
    }
};
</script>

<style></style>
