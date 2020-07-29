const express = require("express");
const cors = require("cors");

app = express();

app.use(cors());

const commands = require("./api/commands");

app.use("/api", commands);

const port = process.env.PORT || 49156;

app.listen(port, () => console.log(`Server started on port ${port}.`));
