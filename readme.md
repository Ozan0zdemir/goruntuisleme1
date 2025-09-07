# Görüntü İşleme Projesi

## Proje Dosyaları

# yazitespitfoto.html

Tarayıcı üzerinden çalışan bir web sitesi aracılığıyla yüklenen fotoğraftaki yazıları tespit etmek için kullanılır. Çalışırken javascrip, Tensorflow ve css gibi teknolojilerden faydalanır.


# eltespit.py

Kamera aracılığıyla el ve parmakları tespit edip parmak sayısını tespit eden bir uygulamadır. Çalışırken MediaPipe Hands kullanarak elin iskeletini ve ana noktalarını tespit eder.

# duygutespit.py

DeepFace teknolojisi kullanarak yüzümüzü analiz eder ve duygularımızı tespit etmeye çalışan bir kod ancak tam olarak çalışmamaktadır çünkü herkesin farklı bir yüz yapısı ve duygu gösteriş şekli vardır, dolayısıyla yarım çalışan bir kod olduğunu söyleyebiliriz.

# yuztespit.py

mediapipe kullanarak kamerada gözüken yüzleri tespit eden bir koddur. Yüzün iskeletini oluşturup gözün orta noktasını işaretler.

## Gereksinimler

- python 3.10.18
homebrew ile kurmak isterseniz "brew install python@3.10"

- requirements.txt dosyasındaki kütüphaneler
"pip install -r requirements.txt" komutu ile indirebilirsiniz
 bunlar ile uğraşmak istemezseniz kurulum.sh isimli dosyayı çalıştırabilrsiniz
eğer ki çalışmazsa pip install yazıp import yazan kütüphaneleri indirmelisniz
