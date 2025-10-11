from flask import Flask, request, jsonify
import threading
import json
from FlagEmbedding import FlagReRanker