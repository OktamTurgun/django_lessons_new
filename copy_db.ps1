# --- Boshlanish ---

# --- Manba va maqsad yo'llarini sozlash ---
$lesson51 = "C:\Users\User\Documents\GitHub\django_lessons_new\lesson_51\news_project"
$lesson52 = "C:\Users\User\Documents\GitHub\django_lessons_new\lesson_52\news_project"

$sourceDB = Join-Path $lesson51 "db.sqlite3"
$destinationDB = Join-Path $lesson52 "db.sqlite3"

$mediaSource = Join-Path $lesson51 "media"
$mediaDestination = Join-Path $lesson52 "media"

# --- db.sqlite3 faylini nusxalash ---
if (Test-Path $destinationDB) {
    Write-Host "Oldingi db.sqlite3 topildi va o'chirilmoqda..."
    Remove-Item $destinationDB
}

Copy-Item $sourceDB $destinationDB
Write-Host "db.sqlite3 muvaffaqiyatli nusxalandi!"

# --- media papkasini tekshirish va nusxalash ---
if (-Not (Test-Path $mediaDestination)) {
    Write-Host "Media papkasi topilmadi, yangi papka yaratilmoqda..."
    New-Item -ItemType Directory -Path $mediaDestination
}

Write-Host "Media papkasi nusxalanmoqda..."
robocopy $mediaSource $mediaDestination /E
Write-Host "Media papkasi muvaffaqiyatli nusxalandi!"

# --- Tugadi ---
Write-Host "`nBarcha nusxalash ishlari yakunlandi! 🎉"
Write-Host "Endi lesson_52 da db va media tayyor."
