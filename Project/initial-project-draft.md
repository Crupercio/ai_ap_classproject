# Initial Project Draft: Character Voice Message Generator

---

## Section 1: Problem Statement

The task is simple to check. A user uploads a short audio sample of a voice and types a message. The app then creates a new audio clip of that voice saying the message. If the clip says the right words, is easy to understand, and sounds like the voice that was uploaded, the app did its job. For this term I am focusing on voice only, not animation. The first version will be in English, and if time allows I will add Spanish and Japanese.

This matters because there is no easy way right now for a regular person to hear a message in a voice they care about. Parents repeat the same things to their kids every day, like eat your vegetables or brush your teeth, and kids tune it out. A message from a favorite character or from grandma can land differently. It also matters for people who lost someone. Hearing a short message in a loved one's voice could mean a lot, but it also means the app has to be built with care and only used with voices people have the right to use.

This is an AI problem and not something a script could solve. A script can only play clips that were already recorded. This app has to create brand new speech in a voice it has only heard from a short audio sample. That takes a trained voice cloning model, not a lookup or a search box.

---

## Section 2: Target Users

The main users are parents of young kids, around 2 to 8 years old. They would reach for the app during daily routines like dinner, bedtime, or brushing teeth, when the same request has been said ten times and the kid still is not listening. A short message from their favorite character or from grandma can get their attention in a way mom and dad can't.

The app is also for special events. A parent could make a clip of a favorite character saying happy birthday to their kid, or a family could send a holiday message in a grandparent's voice. It can also be for people who want to hear a message in the voice of a loved one who passed away.

What would make someone use it a second time is simple. The clip sounds like the person or character, the kid actually reacts to it, and making a new clip takes about a minute. What would make them quit is if the voice sounds robotic or nothing like the original, if it says words wrong, or if it takes too long to make a short message. For a young kid, a voice that sounds almost right but a little off could also feel creepy instead of fun, which would defeat the whole point.

---

## Section 3: Candidate Approach

I think this project mostly needs a pretrained zero-shot voice cloning model rather than finetuning. The model takes the user's text and a reference voice sample as input and generates new speech in that voice. Zero-shot means it can work with a new voice from a short sample without having to train a separate model on that voice. This is closest to prompting, since the reference clip works like a prompt that tells the model which voice to use. If the cloned voices come out poor for certain types of voices, I may try a small amount of finetuning later, but I don't want to plan on it. RAG and agents don't really fit here since the app isn't looking things up or making decisions on its own.

My main model is **Fish Speech V1.5**, an open model I can run myself in Google Colab. I picked it during the Week 2 model comparison because it supports 13 languages, including English, Spanish, and Japanese, which matches my plan to add those later. **XTTS v2** is my backup since it can clone a voice from a 6 second clip. Both models have licensing restrictions that are fine for this class project but would have to be reviewed if this ever became a commercial product.

The hardest part is getting a good clone from short or messy audio. Character clips often have music or sound effects behind the voice, and a family recording from a phone will have background noise. Names are another risk since the model may say a kid's name wrong, and that would ruin the moment. There is also a safety side. The same tech is used in scams, so the app should only clone voices the user has the right to use, keep clips private, and label them as AI made. For loved ones who passed away, the user writes every word, so the app never makes up things the person didn't say.

My idea changed since Week 1. I dropped the lip sync animation to keep the scope realistic. I also widened the idea from only a kid's favorite character, like Pikachu, to any voice the user has permission to use, including family members and loved ones. I also picked Fish Speech over XTTS because of language support.

---

## Section 4: First-Draft Evaluation Plan

I will measure three main things. First is whether the clip says the right words. I will run each clip through Whisper, a speech-to-text model, and compare what it hears to the message that was typed. This gives a word error rate. Second is whether it sounds like the right voice. I will use a speaker similarity score, which compares the cloned clip to the original sample, and I will also have family members rate each clip from 1 to 5 on how much it sounds like the original voice. Third is speed, meaning how long it takes to make one clip.

I will have to build my own test set. I plan to use voice samples from myself and family members who agree to participate, plus a few character-style voices to see how the model handles more exaggerated voices. For each voice I will write around 20 short messages that cover daily routines, birthdays, and messages that use kids' names, including Spanish names. That comes out to at least 100 clips to test. I will also check each name by ear as right or wrong, since saying a kid's name correctly is a big part of what makes the message feel real.

I will also run a smaller subset of the same test messages through XTTS v2 as a baseline. I can compare the two models using the same voice samples and messages to see whether Fish Speech actually performs better in voice similarity, pronunciation, and generation time. This does not need to be the full test set, since Fish Speech is still the main model for the project.

I would call the project a success if it hits these targets:

- Word error rate under 10 percent
- Average family rating of at least 4 out of 5
- Names said correctly at least 90 percent of the time
- A short clip takes under a minute to make

The hardest thing to measure is whether the message actually works on a kid. A clip can score well and still not get my son to eat his vegetables. Whether a voice feels right is also personal, so a similarity score might not match how a family member feels when they hear it. Character-style voices will be tricky too, since they are exaggerated and may score lower even when they sound good to a person.
