import axios from "axios";
import store from "@/store/index";

const apiURL = "http://localhost:49156/api/";

const handleError = fn => (...params) =>
    fn(...params).catch(error => {
        console.log(error);
        const lgmsg = {
            level: "error",
            type: "error",
            message: `Error while communicating with API: ${error.statusText}`
        };
        store.commit("pushLogMessage", lgmsg);
    });

export const api = {
    getText: handleError(async id => {
        const res = await axios.get(apiURL + "text/" + id);
        return res.data;
    }),
    getTexts: handleError(async () => {
        const res = await axios.get(apiURL + "texts");
        return res.data;
    }),
    getTextSentences: handleError(async id => {
        const res = await axios.get(apiURL + "textSentences/" + id);
        return res.data;
    }),
    getSentence: handleError(async id => {
        const res = await axios.get(apiURL + "sentence/" + id);
        return res.data;
    })
};
