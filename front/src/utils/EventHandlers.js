function eventWithoutFrame() {
    return {
        type: "error",
        level: "error",
        message: "Got empty event!"
    };
}

export function processLogEvent(frame) {
    let logMessage;
    if (frame && frame.constructor.name === "Frame") {
        logMessage = JSON.parse(frame.body);
        if (logMessage.error) {
            logMessage["type"] = "error";
            logMessage["level"] = "error";
            logMessage["message"] = logMessage.error;
        }
    } else if (frame && frame.constructor.name === "CloseEvent") {
        logMessage = {
            level: "error",
            type: "error",
            message:
                "Transport is closed. Reason: " +
                frame.reason +
                " Code:" +
                frame.code
        };
    } else {
        logMessage = eventWithoutFrame();
    }
    return logMessage;
}
