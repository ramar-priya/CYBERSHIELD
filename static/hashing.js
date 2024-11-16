let selectedAlgorithm = "";

// Simulated hash dictionary
const hashDictionary = {
  MD5: {
    "5d41402abc4b2a76b9719d911017c592": "hello",
    "098f6bcd4621d373cade4e832627b4f6": "test",
  },
  SHA1: {
    a94a8fe5ccb19ba61c4c0873d391e987982fbbd3: "hello",
    d5579c46dfcc7d0d6a93cb8a89386a55d1fdd35f: "test",
  },
  SHA256: {
    "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824": "hello",
    "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08": "test",
  },
};

function setAlgorithm(algorithm) {
  selectedAlgorithm = algorithm;
  document.getElementById(
    "selectedAlgorithm"
  ).textContent = `Selected Algorithm: ${algorithm}`;
}

function hashText() {
  const text = document.getElementById("inputText").value;
  const output = document.getElementById("outputText");
  if (!selectedAlgorithm) {
    alert("Please select a hashing algorithm.");
    return;
  }
  if (!text) {
    alert("Please enter text to hash.");
    return;
  }

  let hashedValue = "";
  switch (selectedAlgorithm) {
    case "MD5":
      hashedValue = CryptoJS.MD5(text).toString();
      break;
    case "SHA1":
      hashedValue = CryptoJS.SHA1(text).toString();
      break;
    case "SHA256":
      hashedValue = CryptoJS.SHA256(text).toString();
      break;
    default:
      hashedValue = "Unsupported Algorithm";
  }
  output.value = hashedValue;
}

function dehashText() {
  const hash = document.getElementById("inputText").value;
  const output = document.getElementById("outputText");
  if (!selectedAlgorithm) {
    alert("Please select a hashing algorithm.");
    return;
  }
  if (!hash) {
    alert("Please enter a hash to dehash.");
    return;
  }

  const dictionary = hashDictionary[selectedAlgorithm];
  const plaintext = dictionary[hash] || "No match found in dictionary";
  output.value = plaintext;
}
