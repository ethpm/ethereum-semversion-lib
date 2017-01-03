pragma solidity ^0.4.0;

import {SemVersionLib} from "./SemVersionLib.sol";


contract TestSemVersion {
    using SemVersionLib for SemVersionLib.SemVersion;

    SemVersionLib.SemVersion a;
    SemVersionLib.SemVersion b;

    function setA(uint32[3] versionNumbers,
                  string preRelease) public returns (bool) {
        a.init(versionNumbers, preRelease);
    }

    function setB(uint32[3] versionNumbers,
                  string preRelease) public returns (bool) {
        b.init(versionNumbers, preRelease);
    }

    function getA() constant returns (uint32[3], string) {
        return ([a.major, a.minor, a.patch], a.preRelease);
    }

    function getANumIdentifiers() constant returns (uint) {
        return a.preReleaseIdentifiers.length;
    }

    function getAIdentifier(uint idx) constant returns (string) {
        return a.preReleaseIdentifiers[idx];
    }

    function getB() constant returns (uint32[3], string) {
        return ([b.major, b.minor, b.patch], b.preRelease);
    }

    function getBNumIdentifiers() constant returns (uint) {
        return b.preReleaseIdentifiers.length;
    }

    function getBIdentifier(uint idx) constant returns (string) {
        return b.preReleaseIdentifiers[idx];
    }

    function isEqual() constant returns (bool) {
        return a.isEqual(b);
    }

    function isGreater() constant returns (bool) {
        return a.isGreater(b);
    }

    function isLesser() constant returns (bool) {
        return a.isLesser(b);
    }

    function isGreaterOrEqual() constant returns (bool) {
        return a.isGreaterOrEqual(b);
    }

    function isLesserOrEqual() constant returns (bool) {
        return a.isLesserOrEqual(b);
    }
}
