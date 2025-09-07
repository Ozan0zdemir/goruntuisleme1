const upload = document.getElementById('imageUpload');
const statusMessage = document.getElementById('statusMessage');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const result = document.getElementById('result');
const copyButton = document.getElementById('copyButton');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');

upload.addEventListener('change', async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const imageUrl = URL.createObjectURL(file);
  const img = new Image();
  img.onload = async () => {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);

    statusMessage.textContent = 'Metin okunuyor, lütfen bekleyin...';
    statusMessage.style.color = '#3498db';

    // Progress bar göster
    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';

    try {
      const { data } = await Tesseract.recognize(img, 'eng+tur', {
        logger: m => {
          if (m.status === 'recognizing text' && m.progress) {
            const progressPercent = (m.progress * 100).toFixed(0);
            progressBar.style.width = progressPercent + '%';
            statusMessage.textContent = `Metin okunuyor... %${progressPercent}`;
          }
          console.log(m);
        }
      });

      statusMessage.textContent = 'Metin başarıyla çıkarıldı.';
      statusMessage.style.color = '#27ae60';
      progressBar.style.width = '100%';

      result.textContent = data.text.trim();

      // Kelimelerin kutularını çiz
      data.words.forEach(word => {
        const { x0, y0, x1, y1 } = word.bbox;
        ctx.strokeStyle = 'lime';
        ctx.lineWidth = 2;
        ctx.strokeRect(x0, y0, x1 - x0, y1 - y0);
        ctx.fillStyle = 'red';
        ctx.font = '18px sans-serif';
        ctx.fillText(word.text, x0, y0 - 5);
      });

    } catch (err) {
      console.error(err);
      statusMessage.textContent = 'Hata: metin okunamadı.';
      statusMessage.style.color = '#e74c3c';
      progressContainer.style.display = 'none';
    }
  };
  img.src = imageUrl;
});

// Kopyala butonu işlevi
copyButton.addEventListener('click', () => {
  if (!result.textContent.trim()) return;
  navigator.clipboard.writeText(result.textContent)
    .then(() => {
      copyButton.textContent = 'Kopyalandı!';
      setTimeout(() => {
        copyButton.textContent = 'Metni Kopyala';
      }, 2000);
    })
    .catch(() => {
      alert('Kopyalama başarısız oldu.');
    });
});