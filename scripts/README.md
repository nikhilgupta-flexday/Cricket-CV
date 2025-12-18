Batches done:
batches/p5srzthywt9xiobs1sbk82eqfizig2dp83mh
batches/hm6wrzkhgbihyla9wr8jtguaiz477u81930q

Batches for On_lIne:
batches/grouub6xz2i44enalm6sf6m06e99jt11sduj

Batches for off_line
batches/zo2ugxb96qjwitp12gmv09ri4asssoqacd65

# Image Generator

Generate synthetic training data for line-detection models using Gemini.

## Setup

```bash
pip install google-genai python-dotenv
```

Add your API key to `.env` in the project root:
```
GOOGLE_API_KEY=your-api-key
```

## Configuration

Edit the globals at the top of `generate_images.py`:

- `BATCH_SIZE` - number of images to generate
- `ON_LINE` - `True` for foot on line (X prefix), `False` for off line (O prefix)
- `PROMPT` - image generation prompt

## Usage

**Single mode** (immediate, one at a time):
```bash
python generate_images.py single
```

**Batch mode** (async, 50% cheaper, up to 24hr wait):
```bash
python generate_images.py batch
python generate_images.py status <job_name>
python generate_images.py download <job_name>
```

Images save to `scripts/image_results/` with prefix `X_` (on line) or `O_` (off line).