interface Text {
    readonly id: string;
    readonly title: string;
    readonly text: string;
    readonly sentences: Array<string>;
}

interface LogMessage {
    readonly level: string;
    readonly type: string;
    readonly message: string;
}
