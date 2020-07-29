<template>
    <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
            <v-icon :color="statusColor" v-bind="attrs" v-on="on" large>{{
                statusIcon
            }}</v-icon>
        </template>
        <span> {{ statusHint }} </span>
    </v-tooltip>
</template>

<script>
export default {
    name: "TransportAndIndicator",
    data() {
        return {
            statusIcon: "",
            statusColor: "",
            statusHint: ""
        };
    },
    watch: {
        "$store.getters.wStompConnected": function() {
            if (this.$store.getters.wStompConnected) {
                this.statusIcon = "mdi-check-circle";
                this.statusColor = "#44857D";
                this.statusHint = "Web STOMP transport is connected.";
            } else {
                this.statusIcon = "mdi-alert";
                this.statusColor = "#FE6625";
                this.statusHint = "Web STOMP transport is not connected!";
            }
        }
    }
};
</script>

<style></style>
