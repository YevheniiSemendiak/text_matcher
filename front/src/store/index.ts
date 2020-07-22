import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        addTextFormShown: false,
        wStompObj: null,
        textToSend: Array<Text>()
    },
    mutations: {
        flipAddTextFormShown(state) {
            state.addTextFormShown = !state.addTextFormShown;
        },
        addwStompObj(state, wStompObj) {
            if (!state.wStompObj) state.wStompObj = wStompObj;
        },
        pushTextToSend(state, text: Text) {
            state.textToSend.push(text);
        },
        popTextToSend(state) {
            state.textToSend.pop();
        }
    },
    actions: {},
    modules: {},
    getters: {
        textToSend: state => {
            return state.textToSend[state.textToSend.length - 1];
        }
    }
});
