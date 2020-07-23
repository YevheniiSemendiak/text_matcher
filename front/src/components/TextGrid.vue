<template>
    <div>
        <v-container fluid>
            <v-row>
                <template v-for="text in texts">
                    <v-col cols="4" :key="text._id">
                        <text-card
                            :key="text._id"
                            :id="text._id"
                            :title="text.title"
                            :text="text.text"
                        ></text-card>
                    </v-col>
                </template>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import ID from "@/utils/ID";
import TextCard from "@/components/TextCard";

import webstomp from "webstomp-client";

const wStomp = webstomp.over(new WebSocket("ws://rabbit_mq_server:49155/ws"), {
    debug: true
});
wStomp.debug = () => ({}); // disable debug messages from STOMP

export default {
    name: "TextGrid",
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
            texts: this.texts
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
            wStomp.subscribe("front_logs", this.processLogEvent);
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
            this.$store.commit("pushLogMessage", JSON.parse(event.body));
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
        TextCard
    }
};
</script>

<style></style>
