const express = require('express');
const app = express();
const multer = require('multer');
const { exec } = require('child_process');
const axios = require('axios');
const fs = require('fs')
var bodyParser = require('body-parser')
var jsonParser = bodyParser.json()

app.use(jsonParser)


const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, './uploads');
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    console.log(file);
    cb(null, file.fieldname + '-' + uniqueSuffix + '-' + file.originalname);
  }
});

const upload = multer({ storage: storage });

const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});
app.get('/demo', (req, res) => {
  res.sendFile('demo.html', { root: __dirname })
});

app.post('/process', async (req, res) => {
  const filename = `./uploads/${+new Date()}-input.mp4`
  const outputFilename = `./finished/${+new Date()}-output.mp4`

  await downloadVideo(req.body.url, filename);
  console.log(req.body)
  const { frame , xx, xy, yy, yx } = req.body.data;

  await shell(`python3 index.py -v ${filename} -o ${outputFilename} -f ${frame} -xx ${xx} -xy ${xy} -yy ${yy} -yx ${yx}`);
  fs.unlinkSync(filename);
  res.send({ file: outputFilename });
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});


function shell(command) {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        reject(error);
      }
      if (stderr) {
        console.log(stderr);
      }
      resolve(stdout);
    });
  });
}


async function downloadVideo(url, savePath) {
  return new Promise(async (resolve, reject) => {
    const writer = fs.createWriteStream(savePath)

    const response = await axios({
      url,
      method: 'GET',
      responseType: 'stream'
    })

    response.data.pipe(writer)

    // return new Promise((resolve, reject) => {
    writer.on('finish', resolve)
    writer.on('error', reject)
    // })
  })
}

