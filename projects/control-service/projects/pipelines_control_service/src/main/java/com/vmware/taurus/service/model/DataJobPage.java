/*
 * Copyright (c) 2021 VMware, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

package com.vmware.taurus.service.model;

import lombok.Data;

import java.util.List;

@Data
public class DataJobPage {
   private List<Object> content;
   private Integer totalItems;
   private Integer totalPages;
}