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
    methods: {
        clearForm() {
            this.textTitle = "";
            this.text = "";
        },
        submitText() {
            const txt = {
                title: this.textTitle,
                text: this.text
            };
            this.$store.commit("flipAddTextFormShown");
            this.$store.commit("pushTextToSend", txt);
            this.clearForm();
        }
    }
};
</script>

<style></style>
