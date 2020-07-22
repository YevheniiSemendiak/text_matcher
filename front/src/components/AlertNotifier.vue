<template>
    <v-alert
        :type="alertType"
        :value="showAlert"
        dismissible
        class="mx-auto"
        transition="slide-y-transition"
    >
        {{ alertText }}
    </v-alert>
</template>

<script>
export default {
    name: "AlertNotifier",
    props: {
        alertType: {
            required: true,
            type: String
        },
        alertText: {
            required: true,
            type: String
        }
    },
    data() {
        return {
            showAlert: true
        };
    },
    created() {
        setTimeout(() => {
            this.showAlert = false;
        }, 5000);
    }
};
</script>

<style></style>
