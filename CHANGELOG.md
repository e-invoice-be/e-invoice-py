# Changelog

## 1.6.0 (2025-09-02)

Full Changelog: [v1.5.2...v1.6.0](https://github.com/e-invoice-be/e-invoice-py/compare/v1.5.2...v1.6.0)

### Features

* **api:** api update ([b34b73f](https://github.com/e-invoice-be/e-invoice-py/commit/b34b73fe55161a5552ddaf4d90954c7701ce80b7))


### Chores

* **internal:** add Sequence related utils ([1216641](https://github.com/e-invoice-be/e-invoice-py/commit/1216641e3bf60194b65c0010dcf5c3a4c40efc26))

## 1.5.2 (2025-08-27)

Full Changelog: [v1.5.1...v1.5.2](https://github.com/e-invoice-be/e-invoice-py/compare/v1.5.1...v1.5.2)

### Bug Fixes

* avoid newer type syntax ([ea94154](https://github.com/e-invoice-be/e-invoice-py/commit/ea94154de4f824f35864a0d60c7749d0964c9b7f))


### Chores

* **internal:** change ci workflow machines ([fd408d1](https://github.com/e-invoice-be/e-invoice-py/commit/fd408d10ca6538abc22a5b490adb5730e064ff63))
* **internal:** update pyright exclude list ([1ffaa1b](https://github.com/e-invoice-be/e-invoice-py/commit/1ffaa1bcb7dec84e69d7bb7f6fb064940430ec61))
* update github action ([a980eec](https://github.com/e-invoice-be/e-invoice-py/commit/a980eec5b88135e0024646394e9174804f80fa60))

## 1.5.1 (2025-08-12)

Full Changelog: [v1.5.0...v1.5.1](https://github.com/e-invoice-be/e-invoice-py/compare/v1.5.0...v1.5.1)

### Chores

* **internal:** codegen related update ([267c580](https://github.com/e-invoice-be/e-invoice-py/commit/267c580508c1ed14f893c3bc51290429e324c938))
* **internal:** update comment in script ([d094c98](https://github.com/e-invoice-be/e-invoice-py/commit/d094c98404eb3cb780b88a36f008e7d15723d51f))
* update @stainless-api/prism-cli to v5.15.0 ([0a5faff](https://github.com/e-invoice-be/e-invoice-py/commit/0a5faff67bdeebee5ecfc2ddea3f8e0e04ffb50b))

## 1.5.0 (2025-08-08)

Full Changelog: [v1.4.2...v1.5.0](https://github.com/e-invoice-be/e-invoice-py/compare/v1.4.2...v1.5.0)

### Features

* **api:** api update ([1314de4](https://github.com/e-invoice-be/e-invoice-py/commit/1314de4da9421d3aae9893a52384a932c2cafdbe))
* **client:** support file upload requests ([0addd75](https://github.com/e-invoice-be/e-invoice-py/commit/0addd75076181bc078e4b3ca36fac51a0995fb8f))


### Chores

* **internal:** fix ruff target version ([5a9912e](https://github.com/e-invoice-be/e-invoice-py/commit/5a9912efc3fe690afc8b6c2be03733843cb15d7e))
* **project:** add settings file for vscode ([10c5d7a](https://github.com/e-invoice-be/e-invoice-py/commit/10c5d7a8ea652c0eb9bc9cba89da026fcf1cde1b))

## 1.4.2 (2025-07-23)

Full Changelog: [v1.4.1...v1.4.2](https://github.com/e-invoice-be/e-invoice-py/compare/v1.4.1...v1.4.2)

### Bug Fixes

* **parsing:** parse extra field types ([e954db0](https://github.com/e-invoice-be/e-invoice-py/commit/e954db0daa9f76703e2f76ad58eb5865018f0c72))

## 1.4.1 (2025-07-22)

Full Changelog: [v1.4.0...v1.4.1](https://github.com/e-invoice-be/e-invoice-py/compare/v1.4.0...v1.4.1)

### Bug Fixes

* **parsing:** ignore empty metadata ([69c7659](https://github.com/e-invoice-be/e-invoice-py/commit/69c7659042fca8ef93f4a12b053a28e7e303c218))

## 1.4.0 (2025-07-15)

Full Changelog: [v1.3.7...v1.4.0](https://github.com/e-invoice-be/e-invoice-py/compare/v1.3.7...v1.4.0)

### Features

* **api:** manual updates ([001d484](https://github.com/e-invoice-be/e-invoice-py/commit/001d484c462bd0aab6b3a618def015f5fe090abd))
* clean up environment call outs ([4e0d005](https://github.com/e-invoice-be/e-invoice-py/commit/4e0d005d458af9096176a27fec12cd310d84f96d))

## 1.3.7 (2025-07-11)

Full Changelog: [v1.3.6...v1.3.7](https://github.com/e-invoice-be/e-invoice-py/compare/v1.3.6...v1.3.7)

### Bug Fixes

* **client:** don't send Content-Type header on GET requests ([ba60b4e](https://github.com/e-invoice-be/e-invoice-py/commit/ba60b4e67962745385da6dd8a26d60df18af5de0))


### Chores

* **readme:** fix version rendering on pypi ([ceee7c9](https://github.com/e-invoice-be/e-invoice-py/commit/ceee7c97b1a66e52af5d7ebca18a92f7f15c6025))

## 1.3.6 (2025-07-10)

Full Changelog: [v1.3.5...v1.3.6](https://github.com/e-invoice-be/e-invoice-py/compare/v1.3.5...v1.3.6)

### Bug Fixes

* **parsing:** correctly handle nested discriminated unions ([630bd57](https://github.com/e-invoice-be/e-invoice-py/commit/630bd57b4da7fc008a826f38fead3abae23cb865))


### Chores

* **internal:** bump pinned h11 dep ([92fb15f](https://github.com/e-invoice-be/e-invoice-py/commit/92fb15f6eb150c3b8d0169f2bc20686092f6f33e))
* **internal:** codegen related update ([76ca3ed](https://github.com/e-invoice-be/e-invoice-py/commit/76ca3eddfd71f21424ee9bbcabda6f8c6dd46214))
* **package:** mark python 3.13 as supported ([34f3d13](https://github.com/e-invoice-be/e-invoice-py/commit/34f3d130f8def66ce0c8ec3d9ea9c1b0a6a1c961))

## 1.3.5 (2025-07-02)

Full Changelog: [v1.3.4...v1.3.5](https://github.com/e-invoice-be/e-invoice-py/compare/v1.3.4...v1.3.5)

### Chores

* **ci:** change upload type ([bcd6ac8](https://github.com/e-invoice-be/e-invoice-py/commit/bcd6ac855035693ce19312953d8aaf44500065a3))

## 1.3.4 (2025-06-30)

Full Changelog: [v1.3.3...v1.3.4](https://github.com/e-invoice-be/e-invoice-py/compare/v1.3.3...v1.3.4)

### Bug Fixes

* **ci:** correct conditional ([b2fc172](https://github.com/e-invoice-be/e-invoice-py/commit/b2fc1729d01858664d066ad7bb90ff49283fb75f))


### Chores

* **ci:** only run for pushes and fork pull requests ([a2656c6](https://github.com/e-invoice-be/e-invoice-py/commit/a2656c64c2ebc027ecad4cf574afc513031ce459))

## 1.3.3 (2025-06-27)

Full Changelog: [v1.3.2...v1.3.3](https://github.com/e-invoice-be/e-invoice-py/compare/v1.3.2...v1.3.3)

### Bug Fixes

* **ci:** release-doctor — report correct token name ([0c651d2](https://github.com/e-invoice-be/e-invoice-py/commit/0c651d22fa3a4b6ad10304334083ec6f3a3d114b))

## 1.3.2 (2025-06-25)

Full Changelog: [v1.3.1...v1.3.2](https://github.com/e-invoice-be/e-invoice-py/compare/v1.3.1...v1.3.2)

### Chores

* **internal:** codegen related update ([8bdc2f9](https://github.com/e-invoice-be/e-invoice-py/commit/8bdc2f97fcc5a33a18f14295d34188ac3eac1874))
* **internal:** version bump ([8c7a087](https://github.com/e-invoice-be/e-invoice-py/commit/8c7a087843e1a7dde1587da65d8cf505f34d61de))

## 1.3.1 (2025-06-24)

Full Changelog: [v1.3.0...v1.3.1](https://github.com/e-invoice-be/e-invoice-py/compare/v1.3.0...v1.3.1)

### Chores

* **tests:** skip some failing tests on the latest python versions ([4d9aec8](https://github.com/e-invoice-be/e-invoice-py/commit/4d9aec8c5c7934371dde06daa21af5d11aa64eda))

## 1.3.0 (2025-06-23)

Full Changelog: [v1.2.5...v1.3.0](https://github.com/e-invoice-be/e-invoice-py/compare/v1.2.5...v1.3.0)

### Features

* **api:** api update ([58cabf2](https://github.com/e-invoice-be/e-invoice-py/commit/58cabf2574d9485df337393cbaca4b3ba62b74ad))
* **client:** add support for aiohttp ([3b4cd43](https://github.com/e-invoice-be/e-invoice-py/commit/3b4cd43d7e5e8db43f3e10313b23644d4ec36ac3))


### Documentation

* **client:** fix httpx.Timeout documentation reference ([541b277](https://github.com/e-invoice-be/e-invoice-py/commit/541b2776250952e18c6c7d8dc7435e4edbc46027))

## 1.2.5 (2025-06-18)

Full Changelog: [v1.2.4...v1.2.5](https://github.com/e-invoice-be/e-invoice-py/compare/v1.2.4...v1.2.5)

### Bug Fixes

* **tests:** fix: tests which call HTTP endpoints directly with the example parameters ([d6e5d85](https://github.com/e-invoice-be/e-invoice-py/commit/d6e5d851f2026007b07fc5315232acf9fe29c310))


### Chores

* **readme:** update badges ([4cd10bf](https://github.com/e-invoice-be/e-invoice-py/commit/4cd10bf54c1333a55efbf55b3cffa5c364869ee0))

## 1.2.4 (2025-06-17)

Full Changelog: [v1.2.3...v1.2.4](https://github.com/e-invoice-be/e-invoice-py/compare/v1.2.3...v1.2.4)

## 1.2.3 (2025-06-17)

Full Changelog: [v1.2.2...v1.2.3](https://github.com/e-invoice-be/e-invoice-py/compare/v1.2.2...v1.2.3)

### Bug Fixes

* Update README.md ([2140387](https://github.com/e-invoice-be/e-invoice-py/commit/2140387032cf5e6c6fd7c224ff462607f9bce861))

## 1.2.2 (2025-06-17)

Full Changelog: [v1.2.1...v1.2.2](https://github.com/e-invoice-be/e-invoice-py/compare/v1.2.1...v1.2.2)

### Chores

* **ci:** enable for pull requests ([4a70384](https://github.com/e-invoice-be/e-invoice-py/commit/4a70384eebb606b75838dd0fd659961c609dc6c1))
* **internal:** update conftest.py ([6366369](https://github.com/e-invoice-be/e-invoice-py/commit/6366369219a041ea2f7d71adff7612c4bb7ac973))
* **tests:** add tests for httpx client instantiation & proxies ([6fef8c6](https://github.com/e-invoice-be/e-invoice-py/commit/6fef8c6ccd5d4521e66dba0d9ef3d4898728d829))

## 1.2.1 (2025-06-13)

Full Changelog: [v1.2.0...v1.2.1](https://github.com/e-invoice-be/e-invoice-py/compare/v1.2.0...v1.2.1)

### Bug Fixes

* **client:** correctly parse binary response | stream ([ed989c6](https://github.com/e-invoice-be/e-invoice-py/commit/ed989c6ca76282b848a9eb63644fc473b936d86a))
* **pagination:** correct next page check ([37e2dce](https://github.com/e-invoice-be/e-invoice-py/commit/37e2dcebbdf5074a8dfc8d8ccad88c4d11f8c346))


### Chores

* **tests:** run tests in parallel ([0228226](https://github.com/e-invoice-be/e-invoice-py/commit/02282265dfc4e68be31952864fc68eb651117006))

## 1.2.0 (2025-06-12)

Full Changelog: [v1.1.0...v1.2.0](https://github.com/e-invoice-be/e-invoice-py/compare/v1.1.0...v1.2.0)

### Features

* **api:** manual updates ([2fdad47](https://github.com/e-invoice-be/e-invoice-py/commit/2fdad4768cbc674738be3812c7a905b24da1837e))

## 1.1.0 (2025-06-12)

Full Changelog: [v1.0.1...v1.1.0](https://github.com/e-invoice-be/e-invoice-py/compare/v1.0.1...v1.1.0)

### Features

* **api:** manual updates ([25042c2](https://github.com/e-invoice-be/e-invoice-py/commit/25042c2a2a278e2b0a81ad8297616affc7e12d28))

## 1.0.1 (2025-06-11)

Full Changelog: [v1.0.0...v1.0.1](https://github.com/e-invoice-be/e-invoice-py/compare/v1.0.0...v1.0.1)

### Bug Fixes

* typo ([51965e4](https://github.com/e-invoice-be/e-invoice-py/commit/51965e47ba28b7514f67ee968efe9890259e620c))


### Chores

* **internal:** version bump ([a49b9c8](https://github.com/e-invoice-be/e-invoice-py/commit/a49b9c85db76555c37ed3163ac8b9b3400dc7533))

## 1.0.0 (2025-06-10)

Full Changelog: [v0.1.0-alpha.3...v1.0.0](https://github.com/e-invoice-be/e-invoice-py/compare/v0.1.0-alpha.3...v1.0.0)

### Chores

* update SDK settings ([65f8ae5](https://github.com/e-invoice-be/e-invoice-py/commit/65f8ae52060c066d6d88d8b32d0e1437a8cb61cc))

## 0.1.0-alpha.3 (2025-06-10)

Full Changelog: [v0.1.0-alpha.2...v0.1.0-alpha.3](https://github.com/e-invoice-be/e-invoice-py/compare/v0.1.0-alpha.2...v0.1.0-alpha.3)

### Features

* **api:** api update ([f5a8196](https://github.com/e-invoice-be/e-invoice-py/commit/f5a81964419d8777b472990f56365ebdea34c029))
* **client:** add follow_redirects request option ([c395968](https://github.com/e-invoice-be/e-invoice-py/commit/c39596814d57ad3db090a24ff148429679b03f27))


### Chores

* **docs:** remove reference to rye shell ([0dc05f6](https://github.com/e-invoice-be/e-invoice-py/commit/0dc05f6c1c1a8346862155ae23422bd60fee7df3))

## 0.1.0-alpha.2 (2025-05-30)

Full Changelog: [v0.1.0-alpha.1...v0.1.0-alpha.2](https://github.com/e-invoice-be/e-invoice-py/compare/v0.1.0-alpha.1...v0.1.0-alpha.2)

### Features

* **api:** manual updates ([b0954e1](https://github.com/e-invoice-be/e-invoice-py/commit/b0954e1357427a7573685d1e14eb8f7007085568))


### Chores

* sync repo ([d7d024c](https://github.com/e-invoice-be/e-invoice-py/commit/d7d024c67978e805e5fa7c34bda753dd5ca84868))
* update SDK settings ([15f7d70](https://github.com/e-invoice-be/e-invoice-py/commit/15f7d7061d77d0d8f3adc51196fcf11ef1845e1b))

## 0.1.0-alpha.1 (2025-05-30)

Full Changelog: [v0.0.1-alpha.0...v0.1.0-alpha.1](https://github.com/e-invoice-be/e-invoice-api-sdk-py/compare/v0.0.1-alpha.0...v0.1.0-alpha.1)

### Features

* **api:** api update ([83eeaf0](https://github.com/e-invoice-be/e-invoice-api-sdk-py/commit/83eeaf0a5ff0c97328e6e1f9a83ae85401c29b24))
* **api:** manual updates ([8e2b6fd](https://github.com/e-invoice-be/e-invoice-api-sdk-py/commit/8e2b6fdbdf5dbb924730f3d21129822f76c3681b))
* **api:** manual updates ([caf28f0](https://github.com/e-invoice-be/e-invoice-api-sdk-py/commit/caf28f07f11798707e249444f04600a1ac461110))
* **api:** update via SDK Studio ([4dab89b](https://github.com/e-invoice-be/e-invoice-api-sdk-py/commit/4dab89b520bd6891b329a6e0b031468eb7c96948))
* **api:** update via SDK Studio ([3ab411e](https://github.com/e-invoice-be/e-invoice-api-sdk-py/commit/3ab411e843b369f9d3a83596217428c7a663025d))
* **api:** update via SDK Studio ([f21ce20](https://github.com/e-invoice-be/e-invoice-api-sdk-py/commit/f21ce20df9505ccc85d9578b68b3ceade2e70d66))


### Chores

* configure new SDK language ([66045d6](https://github.com/e-invoice-be/e-invoice-api-sdk-py/commit/66045d60d0bada2ccada1e97bc22f62b92215841))
* update SDK settings ([5e9a7d7](https://github.com/e-invoice-be/e-invoice-api-sdk-py/commit/5e9a7d71f7c28d53a849c4766e115af2032c76c8))
