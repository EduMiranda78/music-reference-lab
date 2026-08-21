# -*- coding: utf-8 -*-
"""
Music Reference Lab - Presets and High-Energy Exporter Module
Este módulo implementa presets e mapeamento de heurísticas focado em:
- Alta agitação, movimento, ação e tensão ("Guerra").
- Vocais cariocas personalizados (Voz de Cria masculina rouca com marra / Voz feminina suave e envolvente).
- Exportação compatível com os Schemas A e B para Suno e HeartMuLa.
"""

from typing import Dict, Any, List, Optional


class HighEnergyPresets:
    """
    Biblioteca de Presets focados em Agitação, Movimento, Ação, Tensão e Guerra.
    Converte as métricas do analisador acústico em conjuntos de tags otimizados para Suno e HeartMuLa.
    """

    PRESETS = {
        "guerra_de_cria": {
            "name": "Guerra de Cria (Funk Rj & Phonk Pesado)",
            "description": "Fusão agressiva de Funk Carioca com Phonk industrial, sub-graves distorcidos e batida rítmica implacável.",
            "base_styles": [
                "Brazilian Phonk", "Funk Carioca", "heavy distorted 808 bass",
                "aggressive rhythmic beat", "130-140 BPM", "gritty phonk cowbell",
                "raw street energy", "high-octane tension"
            ],
            "vibe_tags": ["dangerous", "relentless", "combat", "street grit", "heavy brass hits"],
            "vocal_male_tags": [
                "husky male vocal with carioca accent", "raspy aggressive male voice",
                "gritty spoken rap flow", "intense RJ street whisper"
            ],
            "vocal_female_tags": [
                "seductive sultry female vocals", "breathy velvety voice with carioca accent",
                "smooth commanding female voice", "warm dark-pop tone"
            ]
        },
        "acao_epica": {
            "name": "Ação Épica & Guerra Cinemática",
            "description": "Atmosfera de batalha com metais orquestrais dramáticos, tambores de guerra e elementos eletrônicos industriais.",
            "base_styles": [
                "Epic Cinematic Action", "Industrial Rock", "heavy orchestral war drums",
                "dramatic brass stabs", "suspenseful orchestral strings", "hybrid trailer music",
                "overwhelming power"
            ],
            "vibe_tags": ["climax", "battlefield", "high stakes", "militaristic", "unstoppable drive"],
            "vocal_male_tags": [
                "gravelly commanding male vocals", "raspy epic male chanting",
                "gritty speech with heavy reverb"
            ],
            "vocal_female_tags": [
                "ethereal but powerful female vocals", "sultry dramatic female chanting",
                "velvety voice cutting through heavy drums"
            ]
        },
        "cyberpunk_guerra": {
            "name": "Guerra Cibernética (Dark Synthwave & Cyberpunk)",
            "description": "Som eletrônico pesado, industrial, com sintetizadores agressivos e distorcidos, ritmo motorizado implacável.",
            "base_styles": [
                "Dark Synthwave", "Cyberpunk Beat", "heavy distorted synth bass",
                "pounding electronic drums", "industrial techno rhythm", "cyberpunk action theme",
                "110-125 BPM"
            ],
            "vibe_tags": ["futuristic combat", "cyber warfare", "neon dark energy", "motorik drive", "intense suspense"],
            "vocal_male_tags": [
                "cybernetic raspy male voice", "robot-tinged husky male vocal",
                "gritty deep vocoder voice with RJ accent"
            ],
            "vocal_female_tags": [
                "seductive cyber female vocals", "breathy velvety dark-pop voice",
                "smooth futuristic female whispering"
            ]
        },
        "tensa_perseguicao": {
            "name": "Tensão Máxima (Trap de Combate)",
            "description": "Grave de Trap extremamente distorcido (808), hi-hats rápidos, clima de urgência e perseguição.",
            "base_styles": [
                "Aggressive Trap", "combat beat", "rattling hi-hats", "distorted 808 glide",
                "menacing minor-key melody", "140-150 BPM", "high action pace"
            ],
            "vibe_tags": ["high-speed chase", "imminent danger", "dark tension", "adrenaline rush", "relentless"],
            "vocal_male_tags": [
                "gritty aggressive male rap flow", "husky voice with RJ accent",
                "intense raw vocal delivery"
            ],
            "vocal_female_tags": [
                "sultry breathy dark-trap female vocals", "smooth velvety rap style with RJ accent",
                "warm powerful female hook"
            ]
        }
    }

    @classmethod
    def get_preset(cls, key: str) -> Optional[Dict[str, Any]]:
        return cls.PRESETS.get(key)


class ActionHeuristicMapper:
    """
    Analisa métricas acústicas vindas do 'audio_analysis.py' e as traduz
    dinamicamente em tags de alta energia, ação e combate, priorizando o sotaque RJ e vozes customizadas.
    """

    def __init__(self, metrics: Dict[str, Any]):
        """
        :param metrics: Dicionário contendo as métricas de áudio extraídas, como:
                        - bpm (float)
                        - onset_density (float)
                        - percussion_ratio (float)
                        - rms (float)
                        - spectral_centroid (float)
                        - stereo_width (float)
                        - key/scale (str, opcional)
        """
        self.metrics = metrics

    def map_to_action_tags(self) -> List[str]:
        """
        Converte as métricas do analisador em tags de produção para reforçar agitação e ação.
        """
        tags = []

        bpm = self.metrics.get("bpm", 120)
        if bpm >= 130:
            tags.extend(["fast-paced", "relentless drive", "high-octane speed"])
        elif bpm >= 100:
            tags.extend(["midtempo heavy drive", "pounding pulse", "steady march"])
        else:
            tags.extend(["slow-burning heavy tension", "ominous march", "heavy slow-tempo groove"])

        onset_density = self.metrics.get("onset_density", 0.5)
        if onset_density > 0.7:
            tags.extend(["rapid-fire beats", "chaotic energy", "intense wall of sound", "non-stop action"])
        elif onset_density > 0.4:
            tags.extend(["rhythmic movement", "dynamic progression", "active beat"])
        else:
            tags.extend(["sparse heavy hits", "suspenseful silence", "minimalist tension"])

        percussion_ratio = self.metrics.get("percussion_ratio", 0.5)
        if percussion_ratio > 0.6:
            tags.extend(["heavy percussion-driven", "prominent aggressive drums", "uncompromising beat"])
        else:
            tags.extend(["melodic drive", "orchestral textures", "synthesizer-laden combat atmosphere"])

        rms = self.metrics.get("rms", 0.1)
        if rms > 0.15:
            tags.extend(["heavily compressed", "maximum loudness", "in-your-face dynamic", "brickwall limiting"])
        else:
            tags.extend(["creeping quiet tension", "exploding dynamic range", "sudden loudness bursts"])

        spectral_centroid = self.metrics.get("spectral_centroid", 2000)
        if spectral_centroid > 2500:
            tags.extend(["crisp sharp distortion", "screaming high-ends", "industrial harsh textures"])
        else:
            tags.extend(["dark sub-bass focus", "shadowy deep textures", "muffled brooding rumble"])

        stereo_width = self.metrics.get("stereo_width", 0.5)
        if stereo_width > 0.6:
            tags.extend(["wide atmospheric soundstage", "surrounding cinematic depth", "airy reverb"])
        else:
            tags.extend(["mono focused impact", "punchy direct center channel", "claustrophobic tension"])

        return list(dict.fromkeys(tags))


class CustomGenerator:
    """
    Gera o conteúdo final para Suno e HeartMuLa, injetando as diretrizes cariocas e a temática de guerra.
    """

    @staticmethod
    def generate_suno_export(
        lyrics_pt: str,
        title: str,
        preset_key: str,
        heuristic_tags: List[str],
        vocal_gender: str = "male",
        extra_styles: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Gera a estrutura compacta compatível com o Custom Mode do Suno.
        O limite final de 3000 caracteres do JSON é aplicado pela camada exporters.py.
        """
        preset = HighEnergyPresets.get_preset(preset_key)
        if not preset:
            preset = HighEnergyPresets.PRESETS["guerra_de_cria"]

        styles = list(preset["base_styles"])
        styles.extend(preset["vibe_tags"])
        styles.extend(heuristic_tags[:4])

        if vocal_gender == "male":
            vocal_style = ", ".join(preset["vocal_male_tags"])
        else:
            vocal_style = ", ".join(preset["vocal_female_tags"])

        styles.append(vocal_style)

        if extra_styles:
            styles.extend(extra_styles)

        style_string = ", ".join(list(dict.fromkeys(styles)))[:120]

        if vocal_gender == "male":
            vocal_prompt = "[Vocal Masculino Rouco: voz intimista, muita marra, sotaque carioca rj]"
        else:
            vocal_prompt = "[Vocal Feminino Envolvente: voz suave, sensual, sotaque carioca rj, imponente]"

        structured_lyrics = f"[Intro: Batida pesada de guerra, tensão crescendo]\n{vocal_prompt}\n\n"

        lines = lyrics_pt.strip().split("\n")
        section_counter = 0
        for line in lines:
            if line.strip():
                structured_lyrics += line + "\n"
            else:
                section_counter += 1
                if section_counter == 1:
                    structured_lyrics += "\n[Chorus: Explosão de graves, batida acelerada de ação]\n"
                elif section_counter == 2:
                    structured_lyrics += "\n[Bridge: Tensão extrema, batida desacelera, vocal rouco em destaque]\n"
                else:
                    structured_lyrics += "\n[Outro: Batida pesada desaparecendo no eco]\n"

        if "[Outro:" not in structured_lyrics:
            structured_lyrics += "\n[Outro: Fade out, batida pesada rítmica finaliza no eco]"

        exclude_tags = "acoustic guitar, bossa nova, mpb, calm, relaxing, slow jazz, flute, soft chords"

        return {
            "Title": f"{title} (War Mix)",
            "Styles": style_string,
            "Lyrics": structured_lyrics,
            "Exclude": exclude_tags,
            "Weirdness": 25,
            "StyleInfluence": 85,
            "AudioInfluence": 50
        }

    @staticmethod
    def generate_heartmula_export(
        lyrics_pt: str,
        title: str,
        preset_key: str,
        heuristic_tags: List[str],
        vocal_gender: str = "male"
    ) -> Dict[str, Any]:
        """
        Prepara a exportação dedicada ao HeartMuLa baseada na composição orientada por letra e vocal.
        """
        preset = HighEnergyPresets.get_preset(preset_key)
        if not preset:
            preset = HighEnergyPresets.PRESETS["guerra_de_cria"]

        styles = list(preset["base_styles"]) + preset["vibe_tags"] + heuristic_tags[:3]

        if vocal_gender == "male":
            styles.extend(["gritty raspy male vocal", "rj accent"])
            vocal_prompt_heartmula = "<vocal_male_raspy_rj_marra>"
        else:
            styles.extend(["seductive velvety female voice", "rj accent"])
            vocal_prompt_heartmula = "<vocal_female_breathy_rj_smooth>"

        style_tags_string = ", ".join(list(dict.fromkeys(styles)))

        structured_lyrics = "<!-- Structure Directive: High Agitation & War -->\n"
        structured_lyrics += f"{vocal_prompt_heartmula}\n"
        structured_lyrics += "[section: intro, intense battlefield atmosphere]\n\n"

        lines = lyrics_pt.strip().split("\n")
        for line in lines:
            if line.strip():
                structured_lyrics += line + "\n"
            else:
                structured_lyrics += "\n[section: buildup, heavy drop coming]\n"

        structured_lyrics += "\n[section: epic outro]"

        return {
            "title": f"{title} [Action]",
            "style_tags": style_tags_string,
            "structure": "Intro -> Verse -> Chorus -> Drop -> Verse -> Outro",
            "lyrics": structured_lyrics,
            "negative_prompts": "slow tempo, acoustic, bossa nova, mpb, romantic, sweet acoustic guitar"
        }


if __name__ == "__main__":
    print("--- Testando Mapeamento do Music Reference Lab (Preset: Guerra de Cria) ---")

    metricas_exemplo = {
        "bpm": 135.0,
        "onset_density": 0.82,
        "percussion_ratio": 0.75,
        "rms": 0.18,
        "spectral_centroid": 2800.0,
        "stereo_width": 0.65
    }

    mapper = ActionHeuristicMapper(metricas_exemplo)
    tags_geradas = mapper.map_to_action_tags()
    print(f"\nTags Heurísticas Geradas:\n{tags_geradas}")

    letra_usuario = (
        "O asfalto treme com o barulho do motor\n"
        "O cria tá na pista preparado pra ação\n\n"
        "Não adianta correr que a batida já pegou\n"
        "É a tropa avançando no meio do turbilhão"
    )

    suno_res = CustomGenerator.generate_suno_export(
        lyrics_pt=letra_usuario,
        title="Tropa de Ataque",
        preset_key="guerra_de_cria",
        heuristic_tags=tags_geradas,
        vocal_gender="male"
    )

    print("\n=== EXPORTAÇÃO COMPATÍVEL COM SUNO (MALE CO-PROD) ===")
    print(f"Title: {suno_res['Title']}")
    print(f"Styles: {suno_res['Styles']}")
    print(f"Lyrics Preview:\n{suno_res['Lyrics'][:250]}...\n")
    print(f"Exclude: {suno_res['Exclude']}")

    hm_res = CustomGenerator.generate_heartmula_export(
        lyrics_pt=letra_usuario,
        title="Tropa de Ataque",
        preset_key="tensa_perseguicao",
        heuristic_tags=tags_geradas,
        vocal_gender="female"
    )
    print("\n=== EXPORTAÇÃO COMPATÍVEL COM HEARTMULA (FEMALE CO-PROD) ===")
    print(f"Style Tags: {hm_res['style_tags']}")
    print(f"Negative Prompts: {hm_res['negative_prompts']}")
