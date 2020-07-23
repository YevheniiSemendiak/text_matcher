<template>
    <v-snackbar
        app
        :color="alertType"
        :value="showAlert"
        transition="slide-y-reverse-transition"
        bottom
    >
        {{ alertText }}
        <template v-slot:action="{ attrs }">
            <v-btn dark text v-bind="attrs" @click="showAlert = false">
                Close
            </v-btn>
        </template>
    </v-snackbar>
</template>

<script>
export default {
    name: "AlertNotifier",
    data() {
        return {
            showAlert: false,
            alertType: "info",
            alertText: ""
        };
    },
    watch: {
        "$store.getters.lastLogMessage": function() {
            if (this.$store.getters.lastLogMessage) {
                this.alertType = this.$store.getters.lastLogMessage.type;
                this.alertText = this.$store.getters.lastLogMessage.message;
                this.showAlert = true;
                this.$store.commit("popLogMessage");
            }
        }
    }
};
</script>

<style></style>
