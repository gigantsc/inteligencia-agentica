import os
import shutil
import sys

def sync():
    src_base = r"D:\DevCod\inteligencia-agentica"
    dst_base = r"\\100.97.222.112\D\projetos\inteligencia-agentica"
    
    if not os.path.exists(dst_base):
        print(f"⚠️ Destino {dst_base} não acessível no momento (rede/VPN offline ou caminho não montado). Continuando com indexnow e git.")
        return False
        
    dirs_to_copy = ["static", "blog", "content", "tags"]
    files_to_copy = ["sitemap.xml", "llms.txt", "llms-full.txt", "feed.xml", "robots.txt"]
    
    for d in dirs_to_copy:
        src_dir = os.path.join(src_base, d)
        dst_dir = os.path.join(dst_base, d)
        if os.path.exists(src_dir):
            if os.path.exists(dst_dir):
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            print(f"✅ Sincronizado diretório: {d}")
            
    for f in files_to_copy:
        src_file = os.path.join(src_base, f)
        dst_file = os.path.join(dst_base, f)
        if os.path.exists(src_file):
            shutil.copy2(src_file, dst_file)
            print(f"✅ Sincronizado arquivo: {f}")
            
    print("🚀 Sincronização com o servidor concluída com sucesso!")
    return True

if __name__ == "__main__":
    sync()
