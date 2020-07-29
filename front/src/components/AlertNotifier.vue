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
import { processLogEvent } from "@/utils/EventHandlers";

export default {
    name: "AlertNotifier",
    data() {
        return {
            showAlert: false,
            alertType: "info",
            alertText: "",
            logMessages: []
        };
    },
    watch: {
        logMessages: function() {
            if (this.logMessages.length > 0) {
                const logMsg = this.logMessages.shift();
                this.alertType = logMsg.type;
                this.alertText = logMsg.message;
                this.showAlert = true;
            }
        },
        "$store.getters.wStompConnected": function() {
            if (this.$store.getters.wStompConnected) {
                this.$store.getters.wStomp.subscribe("front_logs", event => {
                    this.pushLogMessage(event);
                });
            } else {
                this.logMessages.push({
                    type: "warning",
                    level: "warning",
                    message: "Web STOMP transport was disconnected."
                });
            }
        }
    },
    methods: {
        pushLogMessage(event) {
            this.logMessages.push(processLogEvent(event));
        }
    }
};
</script>

<style></style>
