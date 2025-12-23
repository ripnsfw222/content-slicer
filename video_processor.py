import os
import subprocess
import random
from utils import get_short_path_name

class VideoProcessor:
    def get_video_duration(self, video_path):
        try:
            short_path = get_short_path_name(video_path)
            command = [
                'ffprobe', '-i', short_path, 
                '-show_entries', 'format=duration', 
                '-v', 'quiet', '-of', 'csv=p=0'
            ]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            return float(output.decode('utf-8').strip())
        except Exception as e:
            raise Exception(f"Não foi possível obter a duração do vídeo: {e}")

    def split_video(self, video_path, num_parts):
        try:
            video_path = os.path.abspath(video_path)
            video_folder = os.path.dirname(video_path)
            base_filename = os.path.splitext(os.path.basename(video_path))[0]
            
            short_video_path = get_short_path_name(video_path)
            video_duration = self.get_video_duration(video_path)
            
            part_duration = video_duration / num_parts

            for i in range(num_parts):
                start_time = i * part_duration
                output_filename = f"{base_filename} Part{i+1}.mp4"
                
                command = [
                    'ffmpeg', '-ss', str(start_time), '-i', short_video_path, 
                    '-t', str(part_duration), '-avoid_negative_ts', 'make_zero', 
                    '-c', 'copy', '-y', output_filename
                ]
                subprocess.run(command, check=True, cwd=video_folder, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            return "Vídeo dividido com sucesso!"
        except Exception as e:
            raise e

    def split_by_size(self, video_path, max_size_mb, status_callback=None):
        try:
            video_path = os.path.abspath(video_path)
            video_folder = os.path.dirname(video_path)
            base_filename = os.path.splitext(os.path.basename(video_path))[0]
            
            short_video_path = get_short_path_name(video_path)
            video_duration = self.get_video_duration(video_path)

            total_size_bytes = os.path.getsize(video_path)
            target_size_bytes = max_size_mb * 1024 * 1024
            
            safety_target = target_size_bytes * 0.95
            num_parts = int(total_size_bytes / safety_target) + 1
            part_duration = video_duration / num_parts

            if status_callback:
                status_callback(f"Calculado: {num_parts} partes de ~{max_size_mb}MB")

            for i in range(num_parts):
                start_time = i * part_duration
                output_filename = f"{base_filename} SizePart{i+1}.mp4"
                
                command = [
                    'ffmpeg', '-ss', str(start_time), '-i', short_video_path, 
                    '-t', str(part_duration), '-avoid_negative_ts', 'make_zero', 
                    '-c', 'copy', '-y', output_filename
                ]
                subprocess.run(command, check=True, cwd=video_folder, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            return f"Vídeo dividido em {num_parts} partes com sucesso!"
        except Exception as e:
            raise e

    def random_highlights(self, video_path, num_cuts, cut_duration):
        temp_files = []
        try:
            video_path = os.path.abspath(video_path)
            video_folder = os.path.dirname(video_path)
            base_filename = os.path.splitext(os.path.basename(video_path))[0]
            
            short_video_path = get_short_path_name(video_path)
            video_duration = self.get_video_duration(video_path)
            
            segment_duration = video_duration / num_cuts
            
            for i in range(num_cuts):
                seg_start = i * segment_duration
                seg_end = (i + 1) * segment_duration
                
                max_start = max(seg_start, seg_end - cut_duration)
                start_time = random.uniform(seg_start, max_start)
                
                temp_output = f"temp_h_{i}.mp4"
                temp_files.append(temp_output)
                
                cmd = [
                    'ffmpeg', '-ss', str(start_time), '-i', short_video_path,
                    '-t', str(cut_duration), '-avoid_negative_ts', 'make_zero',
                    '-c', 'copy', '-y', temp_output
                ]
                subprocess.run(cmd, check=True, cwd=video_folder, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)

            list_name = "concat_list.txt"
            list_path = os.path.join(video_folder, list_name)
            temp_files.append(list_name)
            with open(list_path, 'w', encoding='utf-8') as f:
                for tf in temp_files[:-1]:
                    f.write(f"file '{tf}'\n")

            output_filename = f"{base_filename}_Highlights_{num_cuts}x{cut_duration}.mp4"
            
            cmd_concat = [
                'ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_name,
                '-c', 'copy', '-y', output_filename
            ]
            subprocess.run(cmd_concat, check=True, cwd=video_folder, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            return f"Destaques gerados em: {output_filename}"
        except Exception as e:
            raise Exception(f"Erro nos destaques: {str(e)}")
        finally:
            for tf in temp_files:
                try:
                    p = os.path.join(video_folder, tf)
                    if os.path.exists(p): os.remove(p)
                except: pass

    def tiktok_highlights(self, video_path, status_callback=None):
        temp_files = []
        try:
            video_path = os.path.abspath(video_path)
            video_folder = os.path.dirname(video_path)
            base_filename = os.path.splitext(os.path.basename(video_path))[0]
            
            short_video_path = get_short_path_name(video_path)
            video_duration = self.get_video_duration(video_path)
            
            num_cuts = 10
            cut_duration = 5 
            transition_duration = 0.5
            
            if status_callback:
                status_callback("Gerando clipes verticais sequenciais...")
            
            segment_duration = video_duration / num_cuts
            
            for i in range(num_cuts):
                seg_start = i * segment_duration
                seg_end = (i + 1) * segment_duration
                
                max_start = max(seg_start, seg_end - cut_duration)
                start_time = random.uniform(seg_start, max_start)
                
                temp_output = f"tk_temp_{i}.mp4"
                temp_files.append(temp_output)
                
                cmd = [
                    'ffmpeg', '-ss', str(start_time), '-i', short_video_path,
                    '-t', str(cut_duration),
                    '-vf', 'scale=w=1080:h=1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    '-c:a', 'aac', '-ar', '44100', '-y', temp_output
                ]
                subprocess.run(cmd, check=True, cwd=video_folder, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)

            if status_callback:
                status_callback("Aplicando transições e efeitos de alta qualidade...")

            inputs = []
            for tf in temp_files:
                inputs.extend(['-i', tf])
            
            filter_str = ""
            for i in range(num_cuts):
                filter_str += f"[{i}:v]settb=AVTB,setpts=PTS-STARTPTS[v{i}]; "
                filter_str += f"[{i}:a]asetpts=PTS-STARTPTS[a{i}]; "
            
            last_v = "v0"
            last_a = "a0"
            
            for i in range(1, num_cuts):
                offset = (i * cut_duration) - (i * transition_duration)
                next_v = f"v_xf{i}"
                filter_str += f"[{last_v}][v{i}]xfade=transition=fade:duration={transition_duration}:offset={offset}[{next_v}]; "
                last_v = next_v
                
                next_a = f"a_xf{i}"
                filter_str += f"[{last_a}][a{i}]acrossfade=d={transition_duration}:c1=tri:c2=tri[{next_a}]; "
                last_a = next_a
            
            final_v = "vf"
            final_a = "afout" 
            
            total_duration = (num_cuts * cut_duration) - ((num_cuts - 1) * transition_duration)
            fade_start = total_duration - 1.5
            
            filter_str += f"[{last_v}]fade=t=out:st={fade_start}:d=1.5[{final_v}]; "
            filter_str += f"[{last_a}]afade=t=out:st={fade_start}:d=1.5[{final_a}]"

            output_filename = f"{base_filename}_TikTok.mp4"
            
            cmd_final = [
                'ffmpeg'
            ] + inputs + [
                '-filter_complex', filter_str,
                '-map', f'[{final_v}]', '-map', f'[{final_a}]',
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                '-y', output_filename
            ]
            
            subprocess.run(cmd_final, check=True, cwd=video_folder, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            return f"Vídeo para TikTok gerado com sucesso!\nSalvo como: {output_filename}"
            
        except Exception as e:
            raise Exception(f"Erro no TikTok: {str(e)}")
        finally:
            for tf in temp_files:
                try:
                    p = os.path.join(video_folder, tf)
                    if os.path.exists(p): os.remove(p)
                except: pass

    def remove_audio(self, video_path):
        try:
            video_path = os.path.abspath(video_path)
            base, ext = os.path.splitext(video_path)
            video_folder = os.path.dirname(video_path)
            output_filename = f"{os.path.basename(base)}_sem_audio{ext}"
            
            short_video_path = get_short_path_name(video_path)
            
            comando = ['ffmpeg', '-i', short_video_path, '-c', 'copy', '-an', '-y', output_filename]
            subprocess.run(comando, check=True, cwd=video_folder, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            return "Áudio removido com sucesso!"
        except Exception as e:
            raise e
