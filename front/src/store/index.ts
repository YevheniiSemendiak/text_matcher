import Vue from "vue";
import Vuex from "vuex";

import { Client, over } from "webstomp-client";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        addTextFormShown: false,
        texts: Array<Text>(),
        textsIDs: new Set<string>(),
        wStomp: over(
            new WebSocket("ws://" + "localhost" + ":" + 49155 + "/ws"),
            {
                debug: false
            }
        )
    },
    mutations: {
        flipAddTextFormShown(state) {
            state.addTextFormShown = !state.addTextFormShown;
        },
        pushText(state, text: Text) {
            if (!state.textsIDs.has(text._id)) {
                state.textsIDs.add(text._id);
                state.texts.push(text);
            }
        },
        popText(state) {
            const rmvd = state.texts.pop();
            if (rmvd) {
                state.textsIDs.delete(rmvd._id);
            }
        },
        wStomp(state, wStomp: any) {
            state.wStomp = wStomp;
        }
    },
    actions: {},
    modules: {},
    getters: {
        texts(state): Array<Text> {
            return state.texts;
        },
        wStomp(state): Client {
            return state.wStomp;
        },
        wStompConnected(state): boolean {
            return state.wStomp.connected;
        }
    }
});
