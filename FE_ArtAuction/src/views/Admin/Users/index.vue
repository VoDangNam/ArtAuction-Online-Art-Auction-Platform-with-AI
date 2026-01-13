<template>
  <div class="container-fluid py-4 bg-light-subtle">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="text-primary fw-bold mb-1">User Management</h4>
        <p class="text-body-secondary mb-0">Manage access and user information</p>
      </div>
      <router-link to="/admin/add-user" class="btn btn-primary shadow-sm">
        <i class="fa-solid fa-plus me-2"></i>Add New User
      </router-link>
    </div>

    <div class="row g-3 mb-4 animate-fade-in">
      <div class="col-12 col-md-6 col-xl-3">
        <div
          class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-secondary"
        >
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Total Users</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.totalUsers }}</h3>
              </div>
              <div
                class="bg-secondary bg-opacity-10 rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-shield fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Total registered users</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-success">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Active</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.activeUsers }}</h3>
              </div>
              <div
                class="bg-success bg-opacity-10 text-success rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-circle-check fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Currently active</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-info">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Sellers</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.totalSellers }}</h3>
              </div>
              <div
                class="bg-info bg-opacity-10 text-info rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-users fs-5"></i>
              </div>
            </div>
            <small class="text-secondary fw-medium">Total sellers</small>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6 col-xl-3">
        <div class="card border-0 shadow-sm h-100 card-hover border-start border-4 border-danger">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div>
                <h6 class="card-subtitle text-secondary fw-bold mb-1">Locked</h6>
                <h3 class="fw-bold mb-0 text-dark">{{ statistics.totalBlockedUsers }}</h3>
              </div>
              <div
                class="bg-danger bg-opacity-10 text-danger rounded-4 d-flex align-items-center justify-content-center"
                style="width: 48px; height: 48px"
              >
                <i class="fa-solid fa-ban fs-5"></i>
              </div>
            </div>
            <small class="text-danger fw-medium">Policy violation</small>
          </div>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm">
      <div class="card-body">
        <div class="row g-3 mb-4">
          <div class="col-12 col-md-6 col-lg-4">
            <div class="input-group bg-light rounded-pill px-2 border-0">
              <span class="input-group-text bg-transparent border-0 text-secondary">
                <i class="fa-solid fa-magnifying-glass"></i>
              </span>
              <input
                v-model="search"
                type="text"
                class="form-control bg-transparent border-0 shadow-none"
                placeholder="Search by id, name..."
                @input="handleSearch"
              />
            </div>
          </div>
          <div class="col-12 col-md-6 col-lg-8 text-md-end">
            <!-- <button class="btn btn-outline-primary me-2">
              <i class="fa-solid fa-filter me-1"></i> Filter
            </button> -->
            <button
              class="btn btn-outline-primary shadow-sm"
              type="button"
              data-bs-toggle="offcanvas"
              data-bs-target="#offcanvasFilter"
            >
              <i class="fa-solid fa-filter me-1"></i> Filter
            </button>

            <Teleport to="body">
              <div
                class="offcanvas offcanvas-end border-0 shadow-lg"
                tabindex="-1"
                id="offcanvasFilter"
                aria-labelledby="offcanvasFilterLabel"
                style="width: 400px"
              >
                <div class="offcanvas-header border-bottom bg-light-subtle">
                  <div class="d-flex align-items-center gap-2">
                    <div
                      class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center"
                      style="width: 32px; height: 32px"
                    >
                      <i class="fa-solid fa-sliders"></i>
                    </div>
                    <h5 class="offcanvas-title fw-bold text-primary" id="offcanvasFilterLabel">
                      User filter
                    </h5>
                  </div>
                  <div class="modal-header bg-secondary-subtle px-4 py-3 border-0">
                    <button
                      type="button"
                      class="btn-close"
                      @click="closeModal"
                      aria-label="Close"
                    ></button>
                  </div>
                </div>

                <div class="offcanvas-body p-0 flex-grow-1 overflow-y-auto custom-scrollbar-hidden">
                  <div class="p-4">
                    <div class="mb-4">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2"
                        >Status</label
                      >
                      <div class="bg-light rounded-3 p-3 border">
                        <div class="form-check mb-2">
                          <input
                            :value="null"
                            v-model="filterForm.status"
                            class="form-check-input"
                            type="radio"
                            name="statusFilter"
                            id="statusAll"
                            checked
                          />
                          <label class="form-check-label fw-medium" for="statusAll">All</label>
                        </div>
                        <div class="form-check mb-2">
                          <input
                            :value="1"
                            v-model="filterForm.status"
                            class="form-check-input"
                            type="radio"
                            name="statusFilter"
                            id="statusActive"
                          />
                          <label class="form-check-label text-success" for="statusActive"
                            >● Active
                          </label>
                        </div>
                        <div class="form-check mb-2">
                          <input
                            :value="2"
                            v-model="filterForm.status"
                            class="form-check-input"
                            type="radio"
                            name="statusFilter"
                            id="statusLocked"
                          />
                          <label class="form-check-label text-warning" for="statusLocked"
                            >● Locked
                          </label>
                        </div>
                      </div>
                    </div>

                    <hr class="border-secondary opacity-10 my-4" />
                    <!-- Lọc theo role -->
                    <!-- <div class="mb-4">
                      <div class="d-flex align-items-center gap-2 mb-3 text-secondary">
                        <i class="fa-solid fa-user-tag"></i>
                        <label class="form-label fw-bold text-uppercase small mb-0"
                          >Roles & Powers</label
                        >
                      </div>

                      <div class="row g-2">
                        <div class="col-6">
                          <input
                            type="radio"
                            class="btn-check"
                            name="roleFilter"
                            id="roleAll"
                            :value="null"
                            v-model="filterForm.role"
                            checked
                          />
                          <label
                            class="btn btn-outline-secondary w-100 d-flex align-items-center gap-2 py-2 text-start shadow-sm"
                            for="roleAll"
                          >
                            <i class="fa-solid fa-users"></i> All Roles
                          </label>
                        </div>

                        <div class="col-6">
                          <input
                            type="radio"
                            class="btn-check"
                            name="roleFilter"
                            id="roleUser"
                            :value="0"
                            v-model="filterForm.role"
                          />
                          <label
                            class="btn btn-outline-dark w-100 d-flex align-items-center gap-2 py-2 text-start shadow-sm"
                            for="roleUser"
                          >
                            <i class="fa-regular fa-user"></i> User
                          </label>
                        </div>

                        <div class="col-6">
                          <input
                            type="radio"
                            class="btn-check"
                            name="roleFilter"
                            id="roleBuyer"
                            :value="1"
                            v-model="filterForm.role"
                          />
                          <label
                            class="btn btn-outline-info w-100 d-flex align-items-center gap-2 py-2 text-start shadow-sm"
                            for="roleBuyer"
                          >
                            <i class="fa-solid fa-cart-shopping"></i> Buyer
                          </label>
                        </div>

                        <div class="col-6">
                          <input
                            type="radio"
                            class="btn-check"
                            name="roleFilter"
                            id="roleSeller"
                            :value="2"
                            v-model="filterForm.role"
                          />
                          <label
                            class="btn btn-outline-warning w-100 d-flex align-items-center gap-2 py-2 text-start shadow-sm text-dark"
                            for="roleSeller"
                          >
                            <i class="fa-solid fa-store"></i> Seller
                          </label>
                        </div>
                      </div>
                    </div> -->

                    <hr class="border-secondary opacity-10 my-4" />

                    <div class="mb-4">
                      <div class="mb-3">
                        <label class="form-label fw-bold text-uppercase small text-secondary"
                          >Gender</label
                        >
                        <div class="d-flex gap-3">
                          <div class="form-check">
                            <input
                              :value="0"
                              v-model="filterForm.gender"
                              class="form-check-input"
                              type="radio"
                              name="genderFilter"
                              id="genderMale"
                            />
                            <label class="form-check-label" for="genderMale">Male</label>
                          </div>
                          <div class="form-check">
                            <input
                              :value="1"
                              v-model="filterForm.gender"
                              class="form-check-input"
                              type="radio"
                              name="genderFilter"
                              id="genderFemale"
                            />
                            <label class="form-check-label" for="genderFemale">Female</label>
                          </div>
                          <div class="form-check">
                            <input
                              :value="2"
                              v-model="filterForm.gender"
                              class="form-check-input"
                              type="radio"
                              name="genderFilter"
                              id="genderOther"
                            />
                            <label class="form-check-label" for="genderOther">Other</label>
                          </div>
                        </div>
                      </div>

                      <div>
                        <label class="form-label fw-bold text-uppercase small text-secondary"
                          >Province / City</label
                        >
                        <select v-model="filterForm.province" class="form-select shadow-none">
                          <option :value="''" selected>Select area...</option>
                          <option v-for="prov in provinces" :key="prov.id" :value="prov.name">
                            {{ prov.name }}
                          </option>
                        </select>
                      </div>
                    </div>

                    <div class="mb-4">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2"
                        >Date of birth</label
                      >
                      <div class="input-group input-group-sm">
                        <input
                          type="date"
                          class="form-control shadow-none"
                          v-model="filterForm.dateOfBirthFrom"
                          placeholder="From"
                        />
                        <span class="input-group-text bg-light text-secondary">to</span>
                        <input
                          type="date"
                          class="form-control shadow-none"
                          v-model="filterForm.dateOfBirthTo"
                          placeholder="To"
                        />
                      </div>
                    </div>

                    <div class="mb-2">
                      <label class="form-label fw-bold text-uppercase small text-secondary mb-2"
                        >Account creation date</label
                      >

                      <div class="d-flex flex-wrap gap-2 mb-2">
                        <button
                          type="button"
                          class="btn btn-sm border"
                          :class="
                            filterForm.createdAtFilter === 'last7days'
                              ? 'btn-primary text-white'
                              : 'btn-light text-secondary'
                          "
                          @click="setCreatedFilter('last7days')"
                        >
                          Last 7 days
                        </button>
                        <button
                          type="button"
                          class="btn btn-sm border"
                          :class="
                            filterForm.createdAtFilter === 'thismonth'
                              ? 'btn-primary text-white'
                              : 'btn-light text-secondary'
                          "
                          @click="setCreatedFilter('thismonth')"
                        >
                          This month
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="offcanvas-footer border-top p-3 bg-white">
                  <div class="row g-2">
                    <div class="col-4">
                      <button
                        class="btn btn-light border w-100 fw-bold text-secondary"
                        @click="resetFilter"
                      >
                        <i class="fa-solid fa-rotate-right me-1"></i> Reset
                      </button>
                    </div>
                    <div class="col-8">
                      <button
                        class="btn btn-primary w-100 fw-bold shadow-sm"
                        @click="handleFilter"
                        data-bs-dismiss="offcanvas"
                      >
                        Apply
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </Teleport>

            <!-- <button class="btn btn-outline-secondary">
              <i class="fa-solid fa-download me-1"></i> Export
            </button> -->
          </div>
        </div>

        <div class="table-responsive overflow-y-auto custom-scrollbar" style="max-height: 500px">
          <table class="table table-hover align-middle text-nowrap mb-0">
            <thead class="bg-light sticky-top shadow-sm border-bottom border-light-subtle">
              <tr>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase ps-4 py-3">ID</th>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase py-3">User Info</th>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase py-3">Phone</th>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase py-3">Role</th>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase py-3">Address</th>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase py-3">Birthday</th>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase py-3">Gender</th>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase py-3">Status</th>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase py-3">Balance</th>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase py-3">
                  Created At
                </th>
                <th scope="col" class="fw-bold x-small text-dark text-uppercase py-3 text-center">
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="isLoading">
                <td colspan="11" class="text-center py-5 text-muted border-0">
                  <div
                    class="spinner-border spinner-border-sm text-primary mb-2"
                    role="status"
                  ></div>
                  <p class="mb-0 small">Loading user data...</p>
                </td>
              </tr>

              <tr
                v-for="user in sortedUser"
                :key="user.id"
                class="transition-bg border-bottom border-light-subtle"
              >
                <td class="text-secondary fw-medium ps-4">
                  <span class="badge bg-light text-secondary border border-light-subtle"
                    >#{{ user.id }}</span
                  >
                </td>

                <td>
                  <div class="d-flex align-items-center gap-3">
                    <div class="position-relative">
                      <img
                        :src="user.avt"
                        class="rounded-circle border border-2 border-white shadow-sm object-fit-cover"
                        style="width: 40px; height: 40px"
                      />
                    </div>
                    <div>
                      <div class="fw-bold text-dark mb-0" style="font-size: 0.95rem">
                        {{ user.fullname }}
                      </div>
                      <div class="small text-muted" style="font-size: 0.8rem">{{ user.email }}</div>
                    </div>
                  </div>
                </td>

                <td class="text-dark">{{ user.phonenumber }}</td>

                <td>
                  <span
                    class="badge rounded-pill px-3 py-2 border fw-medium"
                    :class="getRoleClass(user.role)"
                  >
                    {{ convertRole(user.role) }}
                  </span>
                </td>

                <td>
                  <span
                    class="d-inline-block text-truncate text-secondary"
                    style="max-width: 150px"
                    :title="user.address"
                  >
                    {{ user.address }}
                  </span>
                </td>

                <td class="text-secondary">{{ user.dateOfBirth }}</td>

                <td>
                  <span
                    class="badge bg-light text-dark border border-light-subtle rounded-pill fw-normal px-2"
                  >
                    <i class="fa-solid fa-venus-mars me-1 text-secondary opacity-50"></i>
                    {{ convertGender(user.gender) }}
                  </span>
                </td>

                <td>
                  <span
                    class="badge rounded-pill border fw-medium px-2 py-1"
                    :class="getStatusClass(user.status)"
                  >
                    <i
                      class="fa-solid fa-circle fa-2xs me-1"
                      :class="
                        user.status === 1
                          ? 'text-success'
                          : user.status === 2
                          ? 'text-danger'
                          : 'text-secondary'
                      "
                    ></i>
                    {{ convertStatus(user.status) }}
                  </span>
                </td>

                <td class="text-success text-end fw-bold">{{ formatCurrency(user.balance) }}</td>

                <td class="small text-muted">{{ formatDate(user.createdAt) }}</td>

                <td class="text-center">
                  <div class="dropdown">
                    <button
                      class="btn btn-sm btn-light btn-action rounded-circle border-0"
                      type="button"
                      data-bs-toggle="dropdown"
                      style="width: 32px; height: 32px"
                    >
                      <i class="fa-solid fa-ellipsis-vertical text-secondary"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end shadow border-0 rounded-3 mt-2">
                      <li>
                        <a class="dropdown-item py-2" @click.prevent="openEditModal(user)">
                          <i class="fa-regular fa-pen-to-square me-2 text-primary"></i>Edit Details
                        </a>
                      </li>
                      <li><hr class="dropdown-divider my-1" /></li>
                      <template v-if="user.status !== 2">
                        <li>
                          <button class="dropdown-item py-2 text-warning" @click="handleLock(user)">
                            <i class="fa-solid fa-lock me-2"></i>Lock Account
                          </button>
                        </li>
                      </template>
                      <template v-if="user.status === 2">
                        <li>
                          <button
                            class="dropdown-item py-2 text-success"
                            @click="handleUnlock(user)"
                          >
                            <i class="fa-solid fa-lock-open me-2"></i>Unlock Account
                          </button>
                        </li>
                      </template>
                      <li>
                        <button
                          class="dropdown-item py-2 text-danger"
                          @click="handleDelete(user.id, user.fullname)"
                        >
                          <i class="fa-regular fa-trash-can me-2"></i>Delete User
                        </button>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination UI -->
        <div class="d-flex justify-content-between align-items-center mt-3" v-if="totalPages > 0">
          <div class="text-secondary small">
            Showing {{ users.length }} of {{ totalElements }} users (Page {{ currentPage + 1 }}/{{ totalPages }})
          </div>
          <nav>
            <ul class="pagination pagination-sm mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 0 }">
                <a class="page-link" href="#" @click.prevent="prevPage">Previous</a>
              </li>
              
              <li 
                class="page-item" 
                v-for="page in visiblePages" 
                :key="page"
                :class="{ active: currentPage === page }"
              >
                <a class="page-link" href="#" @click.prevent="goToPage(page)">{{ page + 1 }}</a>
              </li>
              
              <li class="page-item" :class="{ disabled: currentPage >= totalPages - 1 }">
                <a class="page-link" href="#" @click.prevent="nextPage">Next</a>
              </li>
            </ul>
          </nav>
        </div>

      </div>
    </div>
    <div
      class="modal fade"
      id="editUserModal"
      tabindex="-1"
      aria-hidden="true"
      data-bs-backdrop="static"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
          <div class="modal-header bg-secondary-subtle px-4 py-3 border-0">
            <div class="d-flex align-items-center gap-2">
              <div
                class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center shadow-sm"
                style="width: 40px; height: 40px"
              >
                <i class="fa-solid fa-user-pen"></i>
              </div>
              <div>
                <h5 class="modal-title fw-bold text-primary mb-0">Update User Profile</h5>
                <small class="text-body-secondary">ID: #{{ editingUser.id }}</small>
              </div>
            </div>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>

          <div class="modal-body p-0">
            <div class="row g-0 h-100">
              <div class="col-12 col-lg-4 bg-light-subtle border-end border-light-subtle">
                <div
                  class="d-flex flex-column align-items-center text-center p-4 h-100 justify-content-center"
                >
                  <div class="position-relative mb-3">
                    <img
                      :src="previewAvt || editingUser.avt || 'https://via.placeholder.com/150'"
                      class="rounded-circle shadow-sm border border-4 border-white object-fit-cover"
                      style="width: 150px; height: 150px"
                      alt="User Avatar"
                    />
                    <label
                      for="uploadAvtInput"
                      class="position-absolute bottom-0 end-0 bg-white text-primary border border-2 border-white rounded-circle shadow-sm d-flex align-items-center justify-content-center p-2 mb-1 me-1"
                      style="width: 38px; height: 38px; cursor: pointer"
                    >
                      <i class="fa-solid fa-camera"></i>
                    </label>
                    <input
                      type="file"
                      id="uploadAvtInput"
                      class="d-none"
                      @change="handleFileUpload"
                      accept="image/*"
                    />
                  </div>

                  <h5 class="fw-bold text-dark mb-1">{{ editingUser.fullname }}</h5>
                  <p class="text-secondary small mb-3">{{ editingUser.email }}</p>

                  <div class="d-flex gap-2 justify-content-center w-100">
                    <div class="bg-white rounded-3 p-2 border shadow-sm flex-fill">
                      <small class="d-block text-muted" style="font-size: 0.7rem">BALANCE</small>
                      <span class="fw-bold text-success">{{
                        formatCurrency(editingUser.balance)
                      }}</span>
                    </div>
                    <div class="bg-white rounded-3 p-2 border shadow-sm flex-fill">
                      <small class="d-block text-muted" style="font-size: 0.7rem">CREATED</small>
                      <span class="fw-bold text-dark">{{
                        editingUser.createdAt?.split(" ")[0]
                      }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-12 col-lg-8 bg-white">
                <div class="p-4">
                  <form @submit.prevent="updateUser">
                    <p class="text-uppercase fw-bold text-secondary small mb-3 border-bottom pb-2">
                      <i class="fa-regular fa-id-card me-1"></i> Personal Info
                    </p>

                    <div class="row g-3 mb-4">
                      <div class="col-12">
                        <div class="form-floating">
                          <input
                            type="text"
                            class="form-control bg-light-subtle"
                            id="floatName"
                            v-model="editingUser.fullname"
                            placeholder="Fullname"
                          />
                          <label for="floatName">Full Name</label>
                        </div>
                      </div>

                      <!-- <div class="col-md-6">
                        <div class="form-floating">
                          <input
                            type="date"
                            class="form-control bg-light-subtle"
                            id="floatDob"
                            v-model="editingUser.dateOfBirth"
                            :max="maxDate"
                          />
                          <label for="floatDob">Date of Birth</label>
                        </div>
                      </div> -->
                      <div class="col-md-6">
                        <div class="form-floating">
                          <select
                            class="form-select bg-light-subtle"
                            id="floatGender"
                            v-model="editingUser.gender"
                          >
                            <option :value="0">Male</option>
                            <option :value="1">Female</option>
                            <option :value="2">Other</option>
                          </select>
                          <label for="floatGender">Gender</label>
                        </div>
                      </div>
                    </div>

                    <p class="text-uppercase fw-bold text-secondary small mb-3 border-bottom pb-2">
                      <i class="fa-solid fa-layer-group me-1"></i> Role & Status
                    </p>

                    <div class="row g-3">
                      <div class="col-md-6">
                        <label class="form-label small fw-bold text-secondary">User Role</label>
                        <div class="btn-group w-100" role="group">
                          <input
                            type="radio"
                            class="btn-check"
                            name="roleRadio"
                            id="role0"
                            :value="0"
                            v-model="editingUser.role"
                            autocomplete="off"
                          />
                          <label class="btn btn-outline-secondary btn-sm py-2" for="role0"
                            >User</label
                          >

                          <input
                            type="radio"
                            class="btn-check"
                            name="roleRadio"
                            id="role1"
                            :value="1"
                            v-model="editingUser.role"
                            autocomplete="off"
                          />
                          <label class="btn btn-outline-secondary btn-sm py-2" for="role1"
                            >Buyer</label
                          >

                          <input
                            type="radio"
                            class="btn-check"
                            name="roleRadio"
                            id="role2"
                            :value="2"
                            v-model="editingUser.role"
                            autocomplete="off"
                          />
                          <label class="btn btn-outline-secondary btn-sm py-2" for="role2"
                            >Seller</label
                          >
                        </div>
                      </div>

                      <!-- <div class="col-md-6">
                        <label class="form-label small fw-bold text-secondary"
                          >Account Status</label
                        >
                        <div class="input-group">
                          <span class="input-group-text bg-light-subtle border-end-0">
                            <i
                              class="fa-solid fa-toggle-on"
                              :class="editingUser.status === 1 ? 'text-success' : 'text-danger'"
                            ></i>
                          </span>
                          <select
                            class="form-select bg-light-subtle border-start-0"
                            v-model="editingUser.status"
                          >
                            <option :value="1" class="text-success fw-bold">Active</option>
                            <option :value="0" class="text-danger fw-bold">Locked</option>
                            <option value="Pending approval">Pending</option>
                          </select>
                        </div>
                      </div> -->
                    </div>

                    <div class="mt-4">
                      <div class="form-floating">
                        <input
                          type="text"
                          class="form-control bg-light-subtle"
                          id="floatAddress"
                          v-model="editingUser.address"
                          placeholder="Address"
                        />
                        <label for="floatAddress">Address</label>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer bg-white border-top px-4 py-3">
            <button
              type="button"
              class="btn btn-danger rounded-pill px-4 fw-medium text-light"
              data-bs-dismiss="modal"
              @click="closeModal"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-primary rounded-pill px-4 fw-bold shadow-sm"
              @click="updateUser"
            >
              <i class="fa-regular fa-floppy-disk me-2"></i>Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      users: [],
      isLoading: false,
      search: "",
      statistics: [],
      searchTimeout: null,
      editingUser: {},
      previewAvt: null,
      selectedFile: null, // File thực tế để upload
      modalInstance: null, // Biến giữ instance của Modal

      filterForm: {
        status: null, // null=All, 1=Active, 2=Locked
        gender: null, // null=All, 0=Male, 1=Female, 2=Other
        province: "", // Chuỗi địa chỉ
        dateOfBirthFrom: "",
        dateOfBirthTo: "",
        createdAtFilter: "", // "last7days", "thismonth"
        role: null,
      },
      provinces: [],

      // Pagination state
      currentPage: 0,
      pageSize: 20,
      totalPages: 0,
      totalElements: 0,
    };
  },
  mounted() {
    this.loadUserData();
    this.loadUserStatistical();
    this.fetchProvinces();
  },
  computed: {
    // Không cần reverse nữa vì backend sắp xếp rồi
    sortedUser() {
      return this.users;
    },
    
    // Hiển thị tối đa 5 trang xung quanh trang hiện tại
    visiblePages() {
      const pages = [];
      const maxVisible = 5;
      let startPage = Math.max(0, this.currentPage - Math.floor(maxVisible / 2));
      let endPage = Math.min(this.totalPages - 1, startPage + maxVisible - 1);
      
      if (endPage - startPage + 1 < maxVisible) {
        startPage = Math.max(0, endPage - maxVisible + 1);
      }
      
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }
      return pages;
    },
  },
  methods: {
    // Tối ưu: Load với pagination
    loadUserData() {
      this.isLoading = true;
      axios
        .get(
          `http://localhost:8081/api/admin/lay-du-lieu-user-phan-trang?page=${this.currentPage}&size=${this.pageSize}`,
          {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          }
        )
        .then((res) => {
          this.users = res.data.content;
          this.totalPages = res.data.totalPages;
          this.totalElements = res.data.totalElements;
          console.log(`Loaded page ${this.currentPage + 1}/${this.totalPages}, total: ${this.totalElements}`);
        })
        .catch((err) => {
          console.error(err);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    // Chuyển trang
    goToPage(page) {
      if (page < 0 || page >= this.totalPages) return;
      this.currentPage = page;
      this.loadUserData();
    },

    nextPage() {
      if (this.currentPage < this.totalPages - 1) {
        this.currentPage++;
        this.loadUserData();
      }
    },

    prevPage() {
      if (this.currentPage > 0) {
        this.currentPage--;
        this.loadUserData();
      }
    },
    formatCurrency(value) {
      if (value === null || value === undefined || value === "") {
        return "0 ₫";
      }
      // Trả về định dạng: 100.000 ₫
      return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
      }).format(value);
    },

    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);

      // Tùy chọn định dạng (Format: Oct 22, 2025, 02:30 PM)
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short", // "short" = Oct, "long" = October, "numeric" = 10
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true, // true = AM/PM, false = 24h
      });
    },

    convertStatus(status) {
      switch (status) {
        case 1:
          return "Active";
        case 0:
          return "Inactive";
        case 2:
          return "Locked";
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 1:
          return "bg-success-subtle border-success-subtle text-success";
        case 0:
          return "bg-secondary-subtle border-secondary-subtle text-secondary";
        case 2:
          return "bg-danger-subtle border-danger-subtle text-danger";
      }
    },
    convertRole(roleId) {
      switch (roleId) {
        case 0:
          return "User";
        case 1:
          return "Buyer";
        case 2:
          return "Seller";
        // default:
        //   return "Unknown";
      }
    },

    getRoleClass(roleId) {
      switch (roleId) {
        case 1:
          return "bg-info-subtle border-info-subtle text-info";
        case 0:
          return "bg-secondary-subtle border-secondary-subtle text-secondary";
        case 2:
          return "bg-danger-subtle border-danger-subtle text-danger";
      }
    },

    convertGender(status) {
      switch (status) {
        case 0:
          return "Male";
        case 1:
          return "female";
        case 2:
          return "Other";
        // default:
        //   return "Unknown";
      }
    },

    handleSearch() {
      // Xóa bộ đếm cũ nếu người dùng gõ tiếp khi chưa hết giờ
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }

      // Thiết lập bộ đếm mới (ví dụ: chờ 500ms)
      this.searchTimeout = setTimeout(() => {
        this.performSearchApi(); // Gọi hàm thực thi API sau khi hết giờ chờ
      }, 500);
    },

    performSearchApi() {
      // Nếu ô tìm kiếm trống thì load lại toàn bộ danh sách
      if (!this.search.trim()) {
        this.loadUserData();
        return;
      }
      this.isLoading = true;
      axios
        .get(`http://localhost:8081/api/admin/tim-kiem-user?q=${this.search}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.users = res.data;
          console.log("Kết quả tìm kiếm:", this.users);
        })
        .catch((err) => {
          console.error("Lỗi tìm kiếm:", err);
          this.users = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    // Xóa
    handleDelete(userId, userName) {
      if (!confirm(`Are you sure you want to delete user ${userName}?`)) return;

      axios
        .delete(`http://localhost:8081/api/admin/xoa-user/${userId}`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then(() => {
          alert("Deleted successfully!");
          this.loadUserData();
        })
        .catch((err) => {
          console.error("Error:", err);
          const message = err.response?.data?.message || "Có lỗi xảy ra khi xóa!";
          alert(message);
        });
    },

    //  card thống kê
    loadUserStatistical() {
      axios
        .get(`http://localhost:8081/api/admin/thong-ke-user`, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.statistics = res.data;
          console.log("Kết quả tìm kiếm:", this.statistics);
        })
        .catch((err) => {
          console.error("Lỗi tìm kiếm:", err);
          this.statistics = [];
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    // 1. Hàm mở Modal và đổ dữ liệu
    openEditModal(user) {
      // Clone dữ liệu để không sửa trực tiếp vào bảng khi chưa lưu
      this.editingUser = { ...user };

      // Reset các biến upload ảnh
      this.previewAvt = null;
      this.selectedFile = null;

      // Hiển thị Modal Bootstrap
      const modalElement = document.getElementById("editUserModal");
      // eslint-disable-next-line no-undef
      this.modalInstance = new bootstrap.Modal(modalElement);
      this.modalInstance.show();
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file; // Lưu file vào biến để gửi lên server
        this.previewAvt = URL.createObjectURL(file); // Tạo link ảnh ảo để xem trước
      }
    },

    // Thêm vào trong methods: {}
    toBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
      });
    },

    // Sửa lại hàm updateUser
    async updateUser() {
      if (!this.editingUser.id) return;

      if (this.editingUser.dateOfBirth) {
        const dob = new Date(this.editingUser.dateOfBirth);
        const today = new Date();
        if (dob > today) {
          alert("Date of birth cannot be in the future!");
          return;
        }
      }

      // Tạo object dữ liệu thường (JSON), KHÔNG dùng FormData
      const dataToSend = {
        fullname: this.editingUser.fullname,
        phonenumber: this.editingUser.phonenumber || "",
        address: this.editingUser.address || "",
        gender: this.editingUser.gender,
        role: this.editingUser.role,
        status: this.editingUser.status,
        dateOfBirth: this.editingUser.dateOfBirth || "",
      };

      if (this.selectedFile) {
        try {
          dataToSend.avt = await this.toBase64(this.selectedFile);
        } catch (error) {
          console.error("Lỗi chuyển đổi ảnh:", error);
          return;
        }
      } else {
        // Nếu không chọn ảnh mới, giữ nguyên link ảnh cũ (hoặc null)
        dataToSend.avt = this.editingUser.avt;
      }

      this.isLoading = true;

      // Gửi request dạng JSON (Axios mặc định gửi JSON)
      axios
        .put(`http://localhost:8081/api/admin/cap-nhat-user/${this.editingUser.id}`, dataToSend, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          alert("Information updated successfully!");
          if (this.modalInstance) this.modalInstance.hide();
          this.loadUserData();
        })
        .catch((err) => {
          console.error("Lỗi cập nhật:", err);
          const message = err.response?.data?.message || "Có lỗi xảy ra!";
          alert(message);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    handleLock(user) {
      if (!confirm(`Are you sure you want to block the account: ${user.fullname}?`)) return;
      this.updateUserStatus(user.id, 2);
    },

    handleUnlock(user) {
      if (!confirm(`Do you want to unlock the account: ${user.fullname}?`)) return;
      this.updateUserStatus(user.id, 1);
    },

    updateUserStatus(userId, newStatus) {
      this.isLoading = true;

      const user = this.users.find((u) => u.id === userId);
      const dataToSend = { ...user, status: newStatus };

      axios
        .put(`http://localhost:8081/api/admin/cap-nhat-user/${userId}`, dataToSend, {
          headers: { Authorization: "Bearer " + localStorage.getItem("token") },
        })
        .then(() => {
          if (newStatus === 2) alert("Account blocked successfully!");
          else if (newStatus === 1) alert("Account unlocked!");

          this.loadUserData();
        })
        .catch((err) => {
          console.error("Error:", err);
          alert("An error occurred, please try again!");
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    // Lọc
    handleFilter() {
      this.isLoading = true;

      // chuyển chuỗi rỗng thành null nếu cần thiết
      const payload = {
        status: this.filterForm.status,
        gender: this.filterForm.gender,
        province: this.filterForm.province || null,
        dateOfBirthFrom: this.filterForm.dateOfBirthFrom || null,
        dateOfBirthTo: this.filterForm.dateOfBirthTo || null,
        createdAtFilter: this.filterForm.createdAtFilter || null,
        role: this.filterForm.role,
      };

      axios
        .post("http://localhost:8081/api/admin/loc-user", payload, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        })
        .then((res) => {
          this.users = res.data;
        })
        .catch((err) => {
          console.error("Lỗi bộ lọc:", err);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    resetFilter() {
      this.filterForm = {
        status: null,
        gender: null,
        province: "",
        dateOfBirthFrom: "",
        dateOfBirthTo: "",
        createdAtFilter: "",
        role: null,
      };
      // Sau khi reset thì load lại toàn bộ dữ liệu gốc
      this.loadUserData();
    },
    // Helper để set nhanh thời gian tạo
    setCreatedFilter(val) {
      // Nếu bấm lại vào nút đang active thì bỏ chọn (toggle)
      if (this.filterForm.createdAtFilter === val) {
        this.filterForm.createdAtFilter = "";
      } else {
        this.filterForm.createdAtFilter = val;
      }
    },

    fetchProvinces() {
      axios
        .get("https://open.oapi.vn/location/provinces?page=0&size=63")
        .then((res) => {
          if (res.data && res.data.data) {
            this.provinces = res.data.data;
          }
        })
        .catch((err) => {
          console.error("Lỗi lấy danh sách tỉnh thành:", err);
        });
    },
  },
};
</script>

<style scoped></style>
