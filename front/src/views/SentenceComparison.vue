<template>
    <v-card>
        <v-card-title>
            Similar sentences
            <v-spacer></v-spacer>
            <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                single-line
                label="Search"
                hide-details
            ></v-text-field>
        </v-card-title>
        <v-divider />
        <v-card-subtitle> {{ thisSentence }} </v-card-subtitle>
        <v-data-table
            :headers="tableHeaders"
            :items="items"
            :items-per-page="20"
            class="elevation-5"
            :loading="!loaded"
            :loading-text="tableCaption"
            :search="search"
            multi-sort
            @dblclick:row="onClickRow"
            :footer-props="{
                showFirstLastPage: true,
                firstIcon: 'mdi-arrow-collapse-left',
                lastIcon: 'mdi-arrow-collapse-right',
                prevIcon: 'mdi-arrow-left',
                nextIcon: 'mdi-arrow-right',
                'items-per-page-options': [10, 20, 50, 100, 200, -1]
            }"
        >
        </v-data-table>
    </v-card>
</template>

<script>
import ID from "@/utils/ID";
import { processLogEvent } from "@/utils/EventHandlers";
import { api } from "@/utils/HTTPTransport";

export default {
    name: "SentenceComparison",
    data() {
        return {
            thisSentence: this.$route.params?.sentence,
            thisSentenceID: this.$route.params.sentenceID,
            replyQueueName: "",
            items: [],
            search: "",
            itemsPerPage: 20,
            loaded: false,
            tableCaption: `Searching similar sentences for: ${this.$route.params?.sentence}`,
            tableHeaders: [
                {
                    text: "Text ID",
                    align: "start",
                    sortable: true,
                    value: "textUUID",
                    filterable: true,
                    divider: true
                },
                {
                    text: "Sentence",
                    align: "start",
                    sortable: true,
                    value: "sentence",
                    filterable: true,
                    divider: true
                },
                {
                    text: "Distance",
                    align: "center",
                    sortable: true,
                    value: "distance"
                },
                {
                    text: "Metric",
                    align: "end",
                    sortable: false,
                    value: "metric",
                    filterable: true
                }
            ]
        };
    },
    created() {
        this.replyQueueName = "front-sentComp-" + ID();
        this.wStomp = this.$store.getters.wStomp;
        this.wStomp.subscribe(this.replyQueueName, this.onEvent);
        this.wStomp.send(
            "front_to_back_sentences",
            JSON.stringify({
                sentenceUUID: this.thisSentenceID
            }),
            {
                "reply-to": this.replyQueueName
            }
        );
    },
    methods: {
        onEvent(frame) {
            if (frame) {
                const response = JSON.parse(frame.body);

                if (response.success && response.type === "SentenceDistances") {
                    this.items = response.distances;
                    this.loaded = true;
                } else {
                    this.$store.commit(
                        "pushLogMessage",
                        processLogEvent(frame)
                    );
                }
            } else {
                this.$store.commit("pushLogMessage", processLogEvent(event));
            }
        },
        async onClickRow(rowItem, remData) {
            const text = await api.getText(remData.item?.textUUID);
            this.$router.push({ name: "TextView", params: { text: text } });
        }
    }
};
</script>

<style></style>
