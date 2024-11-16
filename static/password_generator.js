function getRandomCharacter(charSet) {
  const randomIndex = Math.floor(Math.random() * charSet.length);
  return charSet[randomIndex];
}

function generatePassword() {
  const lengthInput = parseInt(document.getElementById("lengthInput").value);
  const includeUppercase = document.getElementById("includeUppercase").checked;
  const includeNumbers = document.getElementById("includeNumbers").checked;
  const includeSymbols = document.getElementById("includeSymbols").checked;
  const wordInput = document.getElementById("wordInput").value;

  const lowercase = "abcdefghijklmnopqrstuvwxyz";
  const uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const numbers = "0123456789";
  const symbols = "!@#$%^&*()_+[]{}|;:,.<>?";

  let charSet = lowercase;
  if (includeUppercase) charSet += uppercase;
  if (includeNumbers) charSet += numbers;
  if (includeSymbols) charSet += symbols;

  let generatedPassword = wordInput;
  const remainingLength = lengthInput - wordInput.length;

  if (remainingLength < 0) {
    document.getElementById("passwordDisplay").innerText =
      "Error: Word length exceeds password length!";
    return;
  }

  for (let i = 0; i < remainingLength; i++) {
    generatedPassword += getRandomCharacter(charSet);
  }

  document.getElementById("passwordDisplay").innerText = generatedPassword;
  updateStrengthMeter(generatedPassword);
}

function updateStrengthMeter(password) {
  const container = document.querySelector(".container");
  const strengthMeter = document.querySelector(".strengthMeter");
  const feedback = document.querySelector(".feedback");

  let strength = 0;

  if (/[A-Z]/.test(password)) strength += 1;
  if (/[0-9]/.test(password)) strength += 1;
  if (/[\W]/.test(password)) strength += 1;

  container.classList.remove("weak", "medium", "strong");
  if (strength === 1) {
    container.classList.add("weak");
  } else if (strength === 2) {
    container.classList.add("medium");
  } else if (strength === 3) {
    container.classList.add("strong");
  }
}

document
  .getElementById("generateBtn")
  .addEventListener("click", generatePassword);
