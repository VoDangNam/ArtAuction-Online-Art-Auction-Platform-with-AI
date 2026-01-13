<template>
	<div class="container py-4">
		<div class="row mb-4 align-items-center">
			<div class="col-12 col-lg-7">
				<h2 class="mb-2">Xác minh ảnh: AI hay Con người</h2>
				<p class="text-muted mb-0">Chọn 1 trong 2 cách: URL test nhanh hoặc tải nhiều ảnh để xác minh.</p>
			</div>
			<div class="col-12 col-lg-5 text-lg-end mt-3 mt-lg-0">
				<div class="btn-group me-2" role="group">
					<input type="radio" class="btn-check" id="mode-url" value="url" v-model="mode">
					<label class="btn btn-outline-dark" for="mode-url">URL test</label>
					<input type="radio" class="btn-check" id="mode-upload5" value="upload5" v-model="mode">
					<label class="btn btn-outline-dark" for="mode-upload5">Upload 5 ảnh</label>
				</div>
				<button class="btn btn-outline-secondary me-2" @click="resetAll" :disabled="submitting">Làm mới</button>
				<button class="btn btn-primary" @click="submit" :disabled="!isReadyToSubmit || submitting">
					<span v-if="!submitting">Gửi xác minh</span>
					<span v-else>
						<span class="spinner-border spinner-border-sm me-2"></span> Đang gửi...
					</span>
				</button>
			</div>
		</div>

		<!-- URL MODE -->
		<div v-if="mode === 'url'" class="row g-4">
			<div class="col-12 col-lg-8">
				<div class="card shadow-sm">
					<div class="card-body">
						<label class="form-label">Đường dẫn ảnh</label>
						<div class="input-group">
							<input type="text" class="form-control" placeholder="https://..." v-model.trim="urlTest.url" @input="onSingleUrlInput">
							<button class="btn btn-outline-secondary" type="button" @click="clearSingleUrl" :disabled="submitting">Xóa</button>
						</div>
						<div class="mt-3">
							<div v-if="urlTest.preview" class="ratio ratio-1x1 border rounded overflow-hidden">
								<img :src="urlTest.preview" alt="preview" style="object-fit: cover;">
							</div>
							<div v-else class="text-muted small">Chưa có ảnh</div>
						</div>
						<div v-if="urlTest.error" class="alert alert-danger py-1 px-2 mt-3 mb-0 small">{{ urlTest.error }}</div>
					</div>
				</div>
			</div>
			<div class="col-12 col-lg-4" v-if="urlTest.result">
				<div class="card h-100 border-0 shadow-sm">
					<div class="card-body">
						<h6 class="mb-2">Kết quả</h6>
						<div class="d-flex align-items-center mb-2">
							<span class="badge" 
								:class="urlTest.result.prediction === 'AI' ? 'bg-danger' : urlTest.result.prediction === 'Human' ? 'bg-success' : 'bg-warning'"
							>
								{{ urlTest.result.prediction }}
							</span>
							<span class="ms-2 text-muted small">AI {{ pct(urlTest.result.ai_probability) }}% • Human {{ pct(urlTest.result.human_probability) }}%</span>
						</div>
						<div class="progress" style="height: 10px;">
							<div class="progress-bar bg-danger" :style="{width: pct(urlTest.result.ai_probability) + '%'}"></div>
							<div class="progress-bar bg-success" :style="{width: pct(urlTest.result.human_probability) + '%'}"></div>
						</div>
						
						<!-- Report buttons for URL Test -->
						<div class="mt-3" v-if="urlTest.result">
							<div class="d-flex gap-2">
								<!-- Unknown: hiện cả 2 nút -->
								<button 
									v-if="urlTest.result.prediction === 'Unknown'" 
									class="btn btn-sm btn-danger" 
									@click="reportUrlImage('AI')"
								>
									Report as AI
								</button>
								<button 
									v-if="urlTest.result.prediction === 'Unknown'" 
									class="btn btn-sm btn-success" 
									@click="reportUrlImage('Human')"
								>
									Report as Human
								</button>
								
								<!-- AI: chỉ hiện Report as Human -->
								<button 
									v-if="urlTest.result.prediction === 'AI'" 
									class="btn btn-sm btn-success" 
									@click="reportUrlImage('Human')"
								>
									Report as Human
								</button>
								
								<!-- Human: chỉ hiện Report as AI -->
								<button 
									v-if="urlTest.result.prediction === 'Human'" 
									class="btn btn-sm btn-danger" 
									@click="reportUrlImage('AI')"
								>
									Report as AI
								</button>
							</div>
							<div v-if="urlTest.reportStatus" class="mt-2 small" :class="urlTest.reportStatus.success ? 'text-success' : 'text-danger'">
								{{ urlTest.reportStatus.message }}
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- UPLOAD MULTI MODE -->
		<div v-else class="row g-4">
			<div class="col-12">
				<div class="card shadow-sm mb-2">
					<div class="card-body d-flex flex-wrap gap-2 align-items-center">
						<input class="form-control" type="file" accept="image/*" multiple @change="onBulkFiles($event)" style="max-width:320px;">
						<button class="btn btn-outline-danger" type="button" @click="removeAll" :disabled="submitting || imageSlots.length===0">Xóa tất cả</button>
						<div class="text-muted small ms-auto">Đã chọn: {{ imageSlots.length }} ảnh</div>
					</div>
				</div>
			</div>
			<div v-for="(slot, idx) in imageSlots" :key="idx" class="col-12 col-sm-6 col-lg-4">
				<div class="card h-100 shadow-sm">
					<div class="card-header bg-white">
						<div class="d-flex justify-content-between align-items-center">
							<strong>Ảnh #{{ idx + 1 }}</strong>
							<select class="form-select form-select-sm" style="max-width:180px;" v-model="slot.viewType">
								<option value="unknown">Góc nhìn (không rõ)</option>
								<option value="front">Chính diện</option>
								<option value="back">Mặt sau</option>
								<option value="angle">Góc nghiêng</option>
								<option value="detail">Cận cảnh/chi tiết</option>
							</select>
						</div>
					</div>
					<div class="card-body">
						<input class="form-control" type="file" accept="image/*" @change="onFileChange(idx, $event)">

						<div class="mt-3 text-center">
							<div v-if="slot.preview" class="ratio ratio-1x1 border rounded overflow-hidden">
								<img :src="slot.preview" alt="preview" style="object-fit: cover;">
							</div>
							<div v-else class="text-muted small">Chưa có ảnh</div>
						</div>

						<div v-if="slot.error" class="alert alert-danger py-1 px-2 mt-3 mb-0 small">{{ slot.error }}</div>
						<div class="d-flex justify-content-end mt-3">
							<button class="btn btn-sm btn-outline-secondary" type="button" @click="removeAt(idx)">Xóa ảnh này</button>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Kết quả -->
		<div v-if="mode === 'upload5' && hasAnyResult" class="row g-4 mt-4">
			<div class="col-12">
				<div class="card shadow-sm">
					<div class="card-body">
						<div class="d-flex flex-column flex-lg-row align-items-lg-center justify-content-lg-between">
							<div class="mb-3 mb-lg-0">
								<h5 class="mb-1">Tổng quan</h5>
								<div class="text-muted small">Trung bình {{ resultSlots.length }} ảnh</div>
							</div>
							<div class="flex-grow-1 px-lg-4 w-100">
								<div class="progress" style="height: 14px;">
									<div class="progress-bar bg-danger" role="progressbar" :style="{width: overall.ai.toFixed(0) + '%'}">AI {{ overall.ai.toFixed(0) }}%</div>
									<div class="progress-bar bg-success" role="progressbar" :style="{width: overall.human.toFixed(0) + '%'}">Human {{ overall.human.toFixed(0) }}%</div>
								</div>
							</div>
							<div class="text-end">
								<span class="badge bg-light text-dark me-1">AI: {{ overall.ai.toFixed(1) }}%</span>
								<span class="badge bg-light text-dark">Human: {{ overall.human.toFixed(1) }}%</span>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div v-for="(slot, idx) in resultSlots" :key="'res-' + idx" class="col-12 col-md-6 col-lg-4">
				<div class="card h-100 border-0 shadow-sm">
					<div class="card-body">
						<div class="d-flex align-items-center mb-3">
							<div class="flex-shrink-0 me-3" style="width:56px;height:56px;">
								<div class="ratio ratio-1x1 rounded border overflow-hidden">
									<img :src="slot.preview" alt="thumb" style="object-fit: cover;">
								</div>
							</div>
							<div class="flex-grow-1">
								<div class="d-flex align-items-center">
									<h6 class="mb-0">Ảnh #{{ idx + 1 }}</h6>
									<span class="ms-2 badge" 
										:class="slot.result.prediction === 'AI' ? 'bg-danger' : slot.result.prediction === 'Human' ? 'bg-success' : 'bg-warning'"
									>
										{{ slot.result.prediction }}
									</span>
								</div>
								<div class="text-muted small">AI {{ pct(slot.result.ai_probability) }}% • Human {{ pct(slot.result.human_probability) }}%</div>
							</div>
						</div>
						<div class="progress" style="height: 10px;">
							<div class="progress-bar bg-danger" :style="{width: pct(slot.result.ai_probability) + '%'}"></div>
							<div class="progress-bar bg-success" :style="{width: pct(slot.result.human_probability) + '%'}"></div>
						</div>
						<div class="mt-2 text-muted small" v-if="slot.result.model_info">
							Model acc: {{ slot.result.model_info.accuracy }} • Epoch: {{ slot.result.model_info.epoch }}
						</div>
						<div class="mt-2" v-if="slot.result">
							<div class="d-flex gap-2">
								<!-- Unknown: hiện cả 2 nút -->
								<button 
									v-if="slot.result.prediction === 'Unknown'" 
									class="btn btn-sm btn-danger" 
									@click="reportImage(idx, 'AI')"
								>
									Report as AI
								</button>
								<button 
									v-if="slot.result.prediction === 'Unknown'" 
									class="btn btn-sm btn-success" 
									@click="reportImage(idx, 'Human')"
								>
									Report as Human
								</button>
								
								<!-- AI: chỉ hiện Report as Human -->
								<button 
									v-if="slot.result.prediction === 'AI'" 
									class="btn btn-sm btn-success" 
									@click="reportImage(idx, 'Human')"
								>
									Report as Human
								</button>
								
								<!-- Human: chỉ hiện Report as AI -->
								<button 
									v-if="slot.result.prediction === 'Human'" 
									class="btn btn-sm btn-danger" 
									@click="reportImage(idx, 'AI')"
								>
									Report as AI
								</button>
							</div>
							<div v-if="slot.reportStatus" class="mt-2 small" :class="slot.reportStatus.success ? 'text-success' : 'text-danger'">
								{{ slot.reportStatus.message }}
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div v-if="globalError" class="alert alert-danger mt-4">{{ globalError }}</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			mode: 'url',
			urlTest: { url: '', preview: null, result: null, error: null, reportStatus: null, downloadedFile: null },
			imageSlots: [],
			submitting: false,
			globalError: null
		};
	},
	computed: {
		isReadyToSubmit() {
			if (this.mode === 'url') {
				return this.isValidUrl(this.urlTest.url);
			}
			return this.imageSlots.length > 0 && this.imageSlots.every((s) => !!s.file);
		},
		hasAnyResult() {
			return this.imageSlots.some((s) => !!s.result);
		},
		resultSlots() {
			return this.imageSlots.filter((s) => !!s.result);
		},
		overall() {
			const results = this.imageSlots.map((s) => s.result).filter(Boolean);
			if (results.length === 0) return { ai: 0, human: 0 };
			const ai = results.reduce((sum, r) => sum + this.ensureNumber(r.ai_probability), 0) / results.length;
			const human = results.reduce((sum, r) => sum + this.ensureNumber(r.human_probability), 0) / results.length;
			return { ai, human };
		}
	},
	methods: {
		async downloadImageToFile(url) {
			// Cố gắng fetch trực tiếp; nếu CORS chặn, thử qua proxy CORS
			const tryFetch = async (u) => {
				const res = await fetch(u, { mode: 'cors' });
				if (!res.ok) throw new Error('HTTP ' + res.status);
				const blob = await res.blob();
				// Chỉ chấp nhận phản hồi thật sự là ảnh
				const isImageMime = (blob.type || '').startsWith('image/');
				if (!isImageMime) throw new Error('URL không trả về nội dung ảnh');
				// Xác định ext hợp lệ
				const allowed = ['jpg','jpeg','png','bmp','webp','tiff'];
				let extFromMime = (blob.type.split('/')[1] || '').toLowerCase();
				let extFromUrl = (u.split('?')[0].match(/\.([a-zA-Z0-9]+)$/) || [,''])[1].toLowerCase();
				let ext = allowed.includes(extFromMime) ? extFromMime : (allowed.includes(extFromUrl) ? extFromUrl : 'jpg');
				const mime = `image/${ext === 'jpg' ? 'jpeg' : ext}`;
				return new File([blob], `remote.${ext}`, { type: mime });
			};
			try {
				return await tryFetch(url);
			} catch (e1) {
				try {
					// Proxy 1
					return await tryFetch(`https://cors.isomorphic-git.org/${encodeURIComponent(url)}`);
				} catch (e2) {
					// Proxy 2 (chuyên ảnh): images.weserv.nl
					const normalized = url.replace(/^https?:\/\//, '');
					return await tryFetch(`https://images.weserv.nl/?url=${encodeURIComponent(normalized)}`);
				}
			}
		},
		onBulkFiles(e) {
			const files = Array.from(e.target.files || []);
			if (files.length === 0) return;
			const newSlots = files.map((f) => ({ 
				file: f, 
				preview: URL.createObjectURL(f), 
				result: null, 
				error: null, 
				viewType: 'unknown',
				reportStatus: null
			}));
			this.imageSlots = [...this.imageSlots, ...newSlots];
		},
		removeAt(index) {
			this.imageSlots.splice(index, 1);
		},
		removeAll() {
			this.imageSlots = [];
		},
		pct(v) {
			return Math.max(0, Math.min(100, Math.round(this.ensureNumber(v))));
		},
		ensureNumber(v) {
			const n = Number(v);
			return Number.isFinite(n) ? n : 0;
		},
		isValidUrl(str) {
			try {
				const u = new URL(str);
				return u.protocol === 'http:' || u.protocol === 'https:';
			} catch (e) {
				return false;
			}
		},
		onFileChange(index, e) {
			const file = e.target.files && e.target.files[0] ? e.target.files[0] : null;
			const slot = this.imageSlots[index];
			slot.file = file;
			slot.error = null;
			slot.preview = file ? URL.createObjectURL(file) : null;
			slot.result = null;
		},
		clearSlot(index) {
			const slot = this.imageSlots[index];
			slot.file = null;
			slot.preview = null;
			slot.result = null;
			slot.error = null;
		},
		resetAll() {
			this.mode = 'url';
			this.urlTest = { url: '', preview: null, result: null, error: null, reportStatus: null, downloadedFile: null };
			this.imageSlots = Array.from({ length: 5 }).map(() => ({ 
				file: null, 
				preview: null, 
				result: null, 
				error: null, 
				viewType: 'unknown',
				reportStatus: null
			}));
			this.globalError = null;
		},
		onSingleUrlInput() {
			this.urlTest.preview = this.isValidUrl(this.urlTest.url) ? this.urlTest.url : null;
			this.urlTest.result = null;
			this.urlTest.error = null;
		},
		clearSingleUrl() {
			this.urlTest = { url: '', preview: null, result: null, error: null, reportStatus: null, downloadedFile: null };
		},
		async reportImage(index, correctLabel) {
			// index is from resultSlots, need to get the actual slot from resultSlots
			const slot = this.resultSlots[index];
			if (!slot || !slot.file || !slot.result) return;
			
			try {
				const form = new FormData();
				form.append('image', slot.file);
				form.append('correct_label', correctLabel);
				
				// Gửi thêm metadata về model prediction SAI
				const wrongPrediction = slot.result.prediction;
				const correctProb = correctLabel === 'AI' 
					? slot.result.ai_probability 
					: slot.result.human_probability;
				
				// Tính wrongProb dựa trên prediction
				let wrongProb;
				if (wrongPrediction === 'AI') {
					wrongProb = slot.result.ai_probability;
				} else if (wrongPrediction === 'Human') {
					wrongProb = slot.result.human_probability;
				} else {
					// Unknown case: model không chắc, dùng probability đối lập với label đúng
					wrongProb = correctLabel === 'AI' 
						? slot.result.human_probability 
						: slot.result.ai_probability;
				}
				
				form.append('wrong_prediction', wrongPrediction);
				form.append('wrong_probability', wrongProb.toFixed(6));
				form.append('correct_probability', correctProb.toFixed(6));
				form.append('confidence_delta', (wrongProb - correctProb).toFixed(6));
				
				const { data } = await axios.post('http://localhost:5000/report', form, {
					headers: { 'Content-Type': 'multipart/form-data' }
				});
				
				slot.reportStatus = { success: true, message: data.message };
				
				// Update the prediction to the correct label after reporting
				slot.result.prediction = correctLabel;
				
				// Optional: Reload model after report
				console.log('Image reported successfully. Consider running quick_train.py to update model.');
			} catch (e) {
				slot.reportStatus = { 
					success: false, 
					message: e?.response?.data?.message || 'Failed to report image' 
				};
			}
		},
		async reportUrlImage(correctLabel) {
			if (!this.urlTest.downloadedFile || !this.urlTest.result) return;
			
			try {
				const form = new FormData();
				form.append('image', this.urlTest.downloadedFile);
				form.append('correct_label', correctLabel);
				
				// Gửi thêm metadata về model prediction SAI
				const wrongPrediction = this.urlTest.result.prediction;
				const correctProb = correctLabel === 'AI' 
					? this.urlTest.result.ai_probability 
					: this.urlTest.result.human_probability;
				
				// Tính wrongProb dựa trên prediction
				let wrongProb;
				if (wrongPrediction === 'AI') {
					wrongProb = this.urlTest.result.ai_probability;
				} else if (wrongPrediction === 'Human') {
					wrongProb = this.urlTest.result.human_probability;
				} else {
					// Unknown case: model không chắc, dùng probability đối lập với label đúng
					wrongProb = correctLabel === 'AI' 
						? this.urlTest.result.human_probability 
						: this.urlTest.result.ai_probability;
				}
				
				form.append('wrong_prediction', wrongPrediction);
				form.append('wrong_probability', wrongProb.toFixed(6));
				form.append('correct_probability', correctProb.toFixed(6));
				form.append('confidence_delta', (wrongProb - correctProb).toFixed(6));
				
				const { data } = await axios.post('http://localhost:5000/report', form, {
					headers: { 'Content-Type': 'multipart/form-data' }
				});
				
				this.urlTest.reportStatus = { success: true, message: data.message };
				
				// Update the prediction to the correct label after reporting
				this.urlTest.result.prediction = correctLabel;
				
				console.log('URL image reported successfully. Consider running quick_train.py to update model.');
			} catch (e) {
				this.urlTest.reportStatus = { 
					success: false, 
					message: e?.response?.data?.message || 'Failed to report image' 
				};
			}
		},
		async submit() {
			if (!this.isReadyToSubmit) {
				this.globalError = this.mode === 'url' ? 'Vui lòng nhập URL hợp lệ.' : 'Vui lòng chọn ít nhất 1 ảnh.';
				return;
			}
			this.globalError = null;
			this.submitting = true;
			try {
				if (this.mode === 'url') {
					// Tải ảnh từ URL về FE (kèm fallback proxy) rồi gửi như upload file
					const file = await this.downloadImageToFile(this.urlTest.url);
					this.urlTest.downloadedFile = file; // Lưu file để dùng cho report sau
					const form = new FormData();
					form.append('image', file);
					const { data } = await axios.post('http://localhost:5000/predict', form);
					this.urlTest.result = data;
					return;
				}

				// Upload N ảnh theo nhóm, đính kèm metadata góc nhìn
				const grouped = new FormData();
				this.imageSlots.forEach((s) => {
					grouped.append('images', s.file);
					grouped.append('view_types[]', s.viewType);
				});

				// Thử endpoint gộp trước; nếu fail, fallback gửi từng ảnh song song
				try {
					const { data } = await axios.post('http://localhost:5000/predict/batch', grouped);
					// Kỳ vọng data.results là mảng độ dài bằng số ảnh gửi lên
					if (data && Array.isArray(data.results) && data.results.length === this.imageSlots.length) {
						data.results.forEach((res, idx) => {
							this.imageSlots[idx].result = res;
							this.imageSlots[idx].error = null;
						});
					} else {
						throw new Error('Batch response không hợp lệ');
					}
				} catch (e) {
					// Fallback: gửi từng ảnh
					const requests = this.imageSlots.map((slot, idx) => {
						const form = new FormData();
						form.append('image', slot.file);
						form.append('view_type', slot.viewType);
					return axios.post('http://localhost:5000/predict', form);
					});
					const res = await Promise.allSettled(requests);
					res.forEach((r, i) => {
						if (r.status === 'fulfilled') {
							this.imageSlots[i].result = r.value.data;
							this.imageSlots[i].error = null;
						} else {
							this.imageSlots[i].result = null;
							this.imageSlots[i].error = r.reason?.response?.data?.message || r.reason?.message || 'Không thể dự đoán ảnh này.';
						}
					});
				}
			} catch (e) {
				this.globalError = e?.response?.data?.message || e?.message || 'Đã xảy ra lỗi khi gửi yêu cầu. Vui lòng thử lại.';
				if (this.mode === 'url') {
					this.urlTest.error = this.globalError;
				}
			} finally {
				this.submitting = false;
			}
		}
	}
};
</script>

<style scoped>
.ratio { position: relative; width: 100%; }
.ratio:before { display: block; content: ""; width: 100%; }
.ratio-1x1:before { padding-top: 100%; }
.ratio > img, .ratio > video, .ratio > iframe, .ratio > .ratio-content {
	position: absolute; top: 0; left: 0; width: 100%; height: 100%;
}
</style>
