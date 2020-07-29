import axios from "axios";

const tmApiPort = process.env.TM_API_PORT || 49156;
const apiURL = `http://tm_api:${tmApiPort}/api/`;

const handleError = fn => (...params) =>
    fn(...params).catch(error => {
        console.log(error);
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
