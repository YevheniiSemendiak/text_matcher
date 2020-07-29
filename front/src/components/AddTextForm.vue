<template>
    <v-row justify="center">
        <v-dialog v-model="$store.state.addTextFormShown" max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="headline">Adding new text</span>
                </v-card-title>
                <v-card-subtitle>
                    <v-container>
                        <v-text-field
                            label="Title"
                            hint="enter text title here"
                            clearable
                            v-model="textTitle"
                        ></v-text-field>
                    </v-container>
                </v-card-subtitle>
                <v-card-text>
                    <v-container>
                        <v-textarea
                            label="Text"
                            placeholder="enter your text here"
                            required
                            clearable
                            outlined
                            auto-grow
                            dense
                            v-model="text"
                            :rules="textValidationRules"
                        ></v-textarea>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="blue-grey darken-4"
                        text
                        @click="clearForm"
                        :disabled="!text && !textTitle"
                        >Clear</v-btn
                    >
                    <v-btn
                        color="blue-grey darken-4"
                        text
                        @click="submitText"
                        :disabled="!text"
                        >Add</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
import ID from "@/utils/ID";
import { api } from "@/utils/HTTPTransport";

export default {
    name: "AddTextForm",
    data() {
        return {
            displayed: true,
            textTitle: "",
            text: "",
            textValidationRules: [value => !!value]
        };
    },
    created() {
        this.replyQueueName = "front-addTextForm-" + ID();
    },
    methods: {
        clearForm() {
            this.textTitle = "";
            this.text = "";
        },
        submitText() {
            this.$store.getters.wStomp.send(
                "front_to_back_text",
                JSON.stringify({
                    title: this.textTitle,
                    text: this.text
                }),
                { "reply-to": this.replyQueueName }
            );
            this.$store.commit("flipAddTextFormShown");
            this.clearForm();
        },
        async textSubmittedCallback(event) {
            if (event.body) {
                const body = JSON.parse(event.body);
                const text = await api.getText(body.textUUID);
                this.$store.commit("pushText", text);
            }
        }
    },
    watch: {
        "$store.getters.wStompConnected": function() {
            if (this.$store.getters.wStompConnected) {
                this.$store.getters.wStomp.subscribe(
                    this.replyQueueName,
                    event => {
                        this.textSubmittedCallback(event);
                    }
                );
            } else {
                this.$store.getters.wStomp.unsubscribe(this.replyQueueName);
            }
        }
    }
};
</script>

<style></style>
