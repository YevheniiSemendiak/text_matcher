interface Text {
    readonly _id: string;
    readonly title: string;
    readonly text: string;
    readonly sentencesUUID: Array<string>;
}

interface LogMessage {
    readonly level: string;
    readonly type: string;
    readonly message: string;
}
