# BlindDev Accessibility Court / HexDrive GenLayer Prototype

A live accessibility adjudication experiment by a blind developer.

The prototype uses GenLayer as an independent adjudication layer for web accessibility audit findings.
It asks validators / LLM-backed adjudication to judge whether an accessibility issue is real, reproducible, and meaningful for users who rely on assistive technology.

## Live demo

- Website: https://hexdrive.tech
- Contract on Bradbury: https://explorer.testnet-chain.genlayer.com/address/0x050fa298a14852FdfB1Bbd8Cd789c0c72d270cdb
- Deployment transaction: https://explorer.testnet-chain.genlayer.com/tx/0x2eea0462e9524d858c923f8b22f94b5cb654302b34647ae68afc26d6fb676042
- Latest adjudication transaction: https://explorer.testnet-chain.genlayer.com/tx/0x2cec79846b583d39e4b4ea38284590656d7dff371160bc8afb10f03fc2ae1303

## Why

Accessibility reports often say what failed, but not whether the issue matters in real usage.
For blind users this difference is important: a technical warning and a real blocker are not the same thing.

This prototype turns accessibility findings into a small adjudication flow:

1. provide page context and the suspected issue;
2. ask GenLayer to judge the accessibility impact;
3. publish provenance links so the report is auditable.

## Contract

The GenLayer intelligent contract is in `contracts/accessibility_court.py`.

It is intentionally small: the goal is to demonstrate the workflow and provenance layer, not to build a full production court yet.

## Project status

Live prototype / experiment.

