// Quantidade de imagens que existem na pasta
const quantidadeDeImagens = 12;

// Container onde os cards serão inseridos
const gallery = document.getElementById('image-gallery');

// Loop para gerar dinamicamente os cards com caminhos locais
for (let i = 1; i <= quantidadeDeImagens; i++) {
  const imgPath = `imagens/img${i}.png`; // Caminho da imagem

  const col = document.createElement('div');
  col.className = "col";

  const card = `
    <div class="image-card text-center">
      <img src="${imgPath}" alt="imagem ${i}" class="img-fluid">
    </div>
  `;

  col.innerHTML = card;
  gallery.appendChild(col);
}
