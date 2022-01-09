import fetchData from './work';
// import flipBit from './work';

async function main() {
  try {
    // flipBit()
    fetchData()
  } catch(e) {
    console.log(e);
  }
}

main()