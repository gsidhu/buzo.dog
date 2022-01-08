const { fetchData } = require('./work');
const { flipBit } = require('./work');

async function main() {
  try {
    flipBit()
    await fetchData()
  } catch(e) {
    console.log(e);
  }
}

flipBit()
// main()