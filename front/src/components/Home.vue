<template>
    <div>
        <alert-notifier
            v-for="(log_obj, index) in logs"
            :key="index"
            :alertType="log_obj.type"
            :alertText="log_obj.message"
        ></alert-notifier>
        <v-container fluid>
            <v-layout wrap justify-space-between>
                <text-card
                    v-for="text in texts"
                    :key="text._id"
                    :id="text._id"
                    :title="text.title"
                    :text="text.text"
                ></text-card>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
import ID from "@/utils/ID";
import TextCard from "@/components/TextCard";
import AlertNotifier from "@/components/AlertNotifier";

import webstomp from "webstomp-client";

const wStomp = webstomp.over(new WebSocket("ws://rabbit_mq_server:49155/ws"));
wStomp.debug = () => ({}); // disable debug messages from STOMP

export default {
    name: "Home",
    debug: true,
    created() {
        this.replyQueueName = "front-" + this.$options.name + "-" + ID();
        this.texts = []; // {id1 : {textTitle: str, text: str}, id2: ...  }
        this.logs = [];
        wStomp.connect(
            "guest", // user
            "guest", // pass
            this.transportConnected,
            this.logEvent,
            "/"
        );
        this.$store.commit("addwStompObj", wStomp);
    },
    destroyed() {
        wStomp.disconnect(this.logEvent);
    },
    data() {
        return {
            texts: this.texts,
            logs: []
        };
    },
    computed: {
        textToSend() {
            return this.$store.textToSend;
        }
    },
    methods: {
        transportConnected() {
            wStomp.subscribe(this.replyQueueName, this.processEvent);
            wStomp.subscribe("logs", this.processLogEvent);
            this.fetchTextData();
        },
        fetchTextData() {
            const dbRequest = {
                collectionName: "Text",
                filter: null,
                projection: null
            };
            wStomp.send("front_to_back_query_db", JSON.stringify(dbRequest), {
                "reply-to": this.replyQueueName
            });
        },
        processEvent(event) {
            const response = JSON.parse(event.body);
            if (!response.success) {
                this.processLogEvent(event);
            } else if (response.type === "QueryDB") {
                this.processQueryDBEvent(response);
            } else if (response.type === "processText") {
                this.logs.push({
                    type: "success",
                    message:
                        "Text with ID " +
                        response.textUUID +
                        " processed successfully."
                });
                const dbRequest = {
                    collectionName: "Text",
                    filter: { _id: response.textUUID },
                    projection: null
                };
                wStomp.send(
                    "front_to_back_query_db",
                    JSON.stringify(dbRequest),
                    {
                        "reply-to": this.replyQueueName
                    }
                );
                console.log(response);
            } else {
                console.log("Unknown event:" + response);
            }
        },
        processQueryDBEvent(response) {
            response.data.forEach(textElem => {
                this.texts.push(textElem);
            });
        },
        processLogEvent(event) {
            const body = JSON.parse(event.body);
            console.log(body);
            this.logs.push(body);
        }
    },
    watch: {
        "$store.getters.textToSend": function() {
            if (this.$store.getters.textToSend) {
                wStomp.send(
                    "front_to_back_text",
                    JSON.stringify(this.$store.getters.textToSend),
                    { "reply-to": this.replyQueueName }
                );
                this.$store.commit("popTextToSend");
            }
        }
    },
    components: {
        TextCard,
        AlertNotifier
    }
};
</script>

<style></style>
