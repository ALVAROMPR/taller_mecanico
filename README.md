# migracioenes incial
# Inicializar migraciones (solo una vez)
flask db init

# Generar primera migración
flask db migrate -m "inicial"

# Aplicar
flask db upgrade

USE nombre_de_tu_basededatos;
ALTER TABLE vehiculo ADD COLUMN anio INT;

# entorno virtual de taller_mecanico
entorno virtual activacion
venv\Scripts\activate

# abrir la carpeta correcta para ejecutar con flask run
(venv) C:\Users\WIN11\Documents\GitHub\taller-mecanico\taller_mecanico>flask run  

# depencias o requisitos necesarios - bibliotecas que estan instaladas en el entorno virtual

si NO existe crearlo:
(venv) C:\Users\WIN11\Documents\GitHub\taller-mecanico>pip freeze > requirements.txt

si existe ejecutar:
pip install -r requirements.txt


# crear un listado de directorio
$rutaBase = "C:\Users\WIN11\Documents\GitHub\taller-mecanico"; $maxItems = 10; $excluir = @("node_modules", ".git", "__pycache__", "bin", "obj", "dist", "build", "plugins", "modulos", "vendor", "cache", "temp", "tmp", ".vs", ".vscode", "packages", "lib"); function Ver($r, $i="", $n=0, $m=3){ if($n -gt $m){return}; $it = Get-ChildItem $r -Force -ErrorAction SilentlyContinue | Where-Object { $excluir -notcontains $_.Name -and $_.Name -notlike ".*" }; $dirs = $it | Where-Object { $_.PSIsContainer }; $files = $it | Where-Object { -not $_.PSIsContainer } | Select-Object -First $maxItems; $c=0; foreach($d in $dirs){ $c++; $pre = if($c -eq $dirs.Count -and $files.Count -eq 0){"└── "}else{"├── "}; Write-Host "$i$pre$($d.Name)\"; $sub = if($c -eq $dirs.Count -and $files.Count -eq 0){"    "}else{"│   "}; Ver $d.FullName "$i$sub" ($n+1) $m }; $fc=0; foreach($f in $files){ $fc++; $pref = if($fc -eq $files.Count){"└── "}else{"├── "}; Write-Host "$i$pref$($f.Name)" }; if($files.Count -ge $maxItems){ Write-Host "$i└── ... limitado a $maxItems archivos" } }; Write-Host "`n=== ESTRUCTURA (sin archivos auto-generados) ===`n" -ForegroundColor Cyan; Ver $rutaBase